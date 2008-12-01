class View(object):
	"""
	This class defines the behavior of the buffer's container.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__set_properties()
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__font_database_uri, MONITOR_FILE, self.__font_changed_cb)
		self.__monid2 = monitor_add(self.__tab_width_database_uri, MONITOR_FILE,
								self.__tab_width_cb)
		self.__monid3 = monitor_add(self.__use_tabs_database_uri, MONITOR_FILE,
								self.__use_tabs_cb)
		self.__monid4 = monitor_add(self.__text_wrapping_database_uri,
								MONITOR_FILE, self.__text_wrapping_cb)
		self.__monid5 = monitor_add(self.__show_margin_database_uri,
								MONITOR_FILE, self.__show_margin_cb)
		self.__monid6 = monitor_add(self.__margin_position_database_uri,
								MONITOR_FILE, self.__margin_position_cb)
		self.__monid7 = monitor_add(self.__spell_check_database_uri,
								MONITOR_FILE, self.__spell_check_cb)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("ready", self.__ready_cb)
		self.__sigid3 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid4 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid5 = self.__view.connect("backspace", self.__backspace_cb)
		self.__sigid6 = editor.connect("readonly", self.__readonly_cb)
		self.__sigid7 = self.__view.connect("drag-motion", self.__drag_motion_cb)
		self.__sigid8 = self.__view.connect("drag-drop", self.__drag_drop_cb)
		self.__sigid9 = self.__view.connect("drag-data-received", self.__drag_data_received_cb)
		self.__sigid10 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid11 = editor.connect("busy", self.__busy_cb)
		self.__sigid12 = editor.connect("refresh", self.__refresh_cb)
		self.__sigid13 = self.__view.connect("move-focus", self.__move_focus_cb)
		editor.register_object(self)
				
	def __init_attributes(self, editor):
		self.__editor = editor
		from gtksourceview2 import View, Buffer
		self.__view = View(Buffer())
		self.__spell_checker = None
		# Path to the font database.
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		syntax_folder = join(editor.metadata_folder, "SyntaxColors")
		font_database_path = join(preference_folder, "Font.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__font_database_uri = get_uri_from_local_path(font_database_path)
		tab_width_database_path = join(preference_folder, "TabWidth.gdb")
		self.__tab_width_database_uri = get_uri_from_local_path(tab_width_database_path)
		use_tabs_database_path = join(preference_folder, "UseTabs.gdb")
		self.__use_tabs_database_uri = get_uri_from_local_path(use_tabs_database_path)
		text_wrapping_database_path = join(preference_folder, "TextWrapping.gdb")
		self.__text_wrapping_database_uri = get_uri_from_local_path(text_wrapping_database_path)
		show_margin_database_path = join(preference_folder, "DisplayRightMargin.gdb")
		self.__show_margin_database_uri = get_uri_from_local_path(show_margin_database_path)
		margin_position_database_path = join(preference_folder, "MarginPosition.gdb")
		self.__margin_position_database_uri = get_uri_from_local_path(margin_position_database_path)
		spell_check_database_path = join(preference_folder, "SpellCheck.gdb")
		self.__spell_check_database_uri = get_uri_from_local_path(spell_check_database_path)
		self.__count = 0
		self.__scrollwin = self.__editor.gui.get_widget("ScrolledWindow")
		return

	def __destroy(self):
		from gnomevfs import monitor_cancel
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__view)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__view)
		self.__editor.disconnect_signal(self.__sigid8, self.__view)
		self.__editor.disconnect_signal(self.__sigid9, self.__view)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor)
		self.__editor.disconnect_signal(self.__sigid11, self.__editor)
		self.__editor.disconnect_signal(self.__sigid12, self.__editor)
		self.__editor.disconnect_signal(self.__sigid13, self.__view)
		if self.__monid1: monitor_cancel(self.__monid1)
		if self.__monid2: monitor_cancel(self.__monid2)
		if self.__monid3: monitor_cancel(self.__monid3)
		if self.__monid4: monitor_cancel(self.__monid4)
		if self.__monid5: monitor_cancel(self.__monid5)
		if self.__monid6: monitor_cancel(self.__monid6)
		if self.__monid7: monitor_cancel(self.__monid7)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		self.__view.set_property("sensitive", True)
		self.__scrollwin.add(self.__view)
		targets = [("text/uri-list", 0, 80)]
		from gtk import DEST_DEFAULT_ALL
		from gtk.gdk import ACTION_COPY, BUTTON1_MASK, ACTION_DEFAULT
		self.__view.drag_dest_set(DEST_DEFAULT_ALL, targets, ACTION_COPY)
		self.__view.set_property("auto-indent", True)
		self.__view.set_property("highlight-current-line", True)
		self.__view.set_property("show-line-numbers", True)
		self.__view.set_property("indent-width", -1)
		from TabWidthMetadata import get_value as tab_width
		self.__view.set_property("tab-width", tab_width())
		from MarginPositionMetadata import get_value as margin_position
		self.__view.set_property("right-margin-position", margin_position())
		from DisplayRightMarginMetadata import get_value as show_margin
		self.__view.set_property("show-right-margin", show_margin())
		from UseTabsMetadata import get_value as use_tabs
		self.__view.set_property("insert-spaces-instead-of-tabs",(not use_tabs()))
		from FontMetadata import get_value as font_name
		from pango import FontDescription
		font = FontDescription(font_name())
		self.__view.modify_font(font)
		from gtk import WRAP_WORD_CHAR, WRAP_NONE
		from TextWrappingMetadata import get_value as wrap_mode_bool
		wrap_mode = self.__view.set_wrap_mode
		wrap_mode(WRAP_WORD_CHAR) if wrap_mode_bool() else wrap_mode(WRAP_NONE)
		self.__scrollwin.show_all()
		from SpellCheckMetadata import get_value as spell_check
		if not spell_check(): return False
		try:
			from gobject import GError
			from gtkspell import Spell
			from locale import getdefaultlocale
			self.__spell_checker = Spell(self.__view, getdefaultlocale()[0])
		except GError:
			pass
		return False

	def __set_readonly(self, readonly):
		self.__view.props.editable = not readonly
		self.__view.props.highlight_current_line = not readonly
		self.__view.props.show_line_numbers = not readonly
		self.__view.props.cursor_visible = not readonly
		self.__refresh()
		return False

	def __sensitive(self, sensitive):
		self.__scrollwin.props.sensitive = sensitive
#		self.__view.props.sensitive = sensitive
		return False
	
	def __refresh(self):
		try:
			self.__view.queue_draw()
			self.__view.queue_resize()
			self.__view.resize_children()
#			self.__view.window.process_updates(True)
		except:
			pass
		finally:
			self.__view.grab_focus()
			self.__editor.response()
		return False

################################################################################
#
#							Signal Listeners
#
################################################################################

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, editor, sensitive):
		self.__sensitive(not sensitive)
		if not sensitive: self.__refresh()
		return False

	def __ready_cb(self, *args):
		self.__sensitive(True)
		self.__refresh()
		return False

	def __checking_file_cb(self, *args):
		self.__view.freeze_child_notify()
		self.__editor.busy()
		return False

	def __loaded_file_cb(self, *args):
		self.__view.thaw_child_notify()
		self.__editor.busy(False)
		self.__refresh()
		return False

	def __load_error_cb(self, *args):
		self.__editor.busy(False)
		self.__refresh()
		return False

	def __readonly_cb(self, editor, readonly, *args):
		self.__set_readonly(readonly)
		return False

	def __backspace_cb(self, *args):
		self.__editor.response()
		return False

	def __drag_motion_cb(self, textview, context, x, y, time):
		if "text/uri-list" in context.targets: return True
		return False

	def __drag_drop_cb(self, textview, context, x, y, time):
		if "text/uri-list" in context.targets: return True
		return False

	def __drag_data_received_cb(self, textview, context, xcord, ycord,
								selection_data, info, timestamp):
		if not ("text/uri-list" in context.targets): return False
		if info != 80: return False
		# Load file
		uri_list = list(selection_data.get_uris())
		self.__editor.open_files(uri_list, None)
		context.finish(True, False, timestamp)
		return True

	def __refresh_cb(self, *args):
		self.__refresh()
		return False

################################################################################
#
#					Preferences Database Listeners
#
################################################################################

	def __font_changed_cb(self, *args):
		from pango import FontDescription
		from FontMetadata import get_value
		new_font = FontDescription(get_value())
		self.__view.modify_font(new_font)
		return

	def __tab_width_cb(self, *args):
		from TabWidthMetadata import get_value
		self.__view.set_tab_width(get_value())
		return

	def __text_wrapping_cb(self, *args):
		from gtk import WRAP_NONE, WRAP_WORD_CHAR
		from TextWrappingMetadata import get_value
		wrap_mode = self.__view.set_wrap_mode
		wrap_mode(WRAP_WORD_CHAR) if get_value() else wrap_mode(WRAP_NONE)
		return

	def __margin_position_cb(self, *args):
		from MarginPositionMetadata import get_value
		self.__view.set_property("right-margin-position", get_value())
		return

	def __show_margin_cb(self, *args):
		from DisplayRightMarginMetadata import get_value
		self.__view.set_property("show-right-margin", get_value())
		return

	def __spell_check_cb(self, *args):
		from SpellCheckMetadata import get_value
		if get_value():
			from gobject import GError
			try:
				from gtkspell import Spell
				from locale import getdefaultlocale
				self.__spell_checker = Spell(self.__view, getdefaultlocale()[0])
			except GError:
				pass
		else:
			try:
				self.__spell_checker.detach()
			except AttributeError:
				pass # For some reason self.__spell_checker is None
		return

	def __use_tabs_cb(self, *args):
		from UseTabsMetadata import get_value
		self.__view.set_insert_spaces_instead_of_tabs(not get_value())
		return

	def __move_focus_cb(self, *args):
		self.__view.stop_emission("move-focus")
		return True
