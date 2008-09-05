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
		editor.register_object(self)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		scrollwin = editor.gui.get_widget("ScrolledWindow")
		scrollwin.add(self.__view)
		scrollwin.set_property("sensitive", True)

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
		return

	def __set_properties(self):
		self.__view.set_property("sensitive", True)
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

	def __destroy(self):
		from gnomevfs import monitor_cancel
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
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

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __font_changed_cb(self, *args):
		from pango import FontDescription
		from FontMetadata import get_value
		new_font = FontDescription(get_value())
		self.__view.modify_font(new_font)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __tab_width_cb(self, *args):
		from TabWidthMetadata import get_value
		self.__view.set_tab_width(get_value())
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __text_wrapping_cb(self, *args):
		from gtk import WRAP_NONE, WRAP_WORD_CHAR
		from TextWrappingMetadata import get_value
		if get_value():
			self.__view.set_wrap_mode(WRAP_WORD_CHAR)
		else:
			self.__view.set_wrap_mode(WRAP_NONE)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __margin_position_cb(self, *args):
		from MarginPositionMetadata import get_value
		self.__view.set_right_margin(int(get_value()))
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __show_margin_cb(self, *args):
		from DisplayRightMarginMetadata import get_value
		self.__view.set_show_right_margin(get_value())
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __spell_check_cb(self, *args):
		from SpellCheckMetadata import get_value
		if get_value():
			from gobject import GError
			try:
				from gtkspell import Spell
				from locale import getdefaultlocale
				self.__spell_checker = Spell(self, getdefaultlocale()[0])
			except GError:
				pass
		else:
			try:
				self.__spell_checker.detach()
			except AttributeError:
				pass # For some reason self.__spell_checker is None
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __use_tabs_cb(self, *args):
		from UseTabsMetadata import get_value
		use_tabs = get_value()
		self.__view.set_insert_spaces_instead_of_tabs(not use_tabs)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

	def __syntax_cb(self, *args):
#		from syntax import activate_syntax_highlight
#		from utils import get_language
#		if not self.__editor.language: return
#		activate_syntax_highlight(self.get_property("buffer"), self.__editor.language)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh_view, priority=PRIORITY_LOW)
		return

#	def __refresh_cb(self, *args):
#		from gobject import idle_add
#		idle_add(self.__refresh, priority=5000)
#		return False
#
#	def __refresh_view(self):
#		self.grab_focus()
#		from gobject import idle_add
#		idle_add(self.__refresh, priority=5000)
#		return False
#
#	def __refresh(self):
#		self.__view.queue_draw()
#		self.__view.queue_resize()
#		self.__view.resize_children()
#		try:
#			self.__view.window.process_updates(True)
#		except:
#			pass
#		return False
