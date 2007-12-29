# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module implements a class that creates a container for the text editor's
buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtksourceview import SourceView

class ScribesTextView(SourceView):
	"""
	This class creates the container object that holds the text editor's buffer.
	It defines the state, properties and behavior of the container object,
	popular called the text editor's view. The view also defines the look and
	feel of the buffer. The color of text in the buffer, the size of fonts, the
	width of tabs are all defined by the view. As such the view is the only
	user customizable part of the text editor. The class inherits from
	gtksourceview.SourceView. See the PyGTK, or GTK+, manual for details on the
	gtksourceview.SourceView class.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: Reference to the text editor instance.
		@type editor: An Editor object.
		"""
		SourceView.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		# Monitor signals and events.
		self.__signal_id_1 = self.connect("map-event", self.__map_event_cb)
		self.__signal_id_2 = self.connect("focus-in-event", self.__focus_in_event_cb)
		self.__signal_id_3 = self.connect("drag-motion", self.__drag_motion_cb)
		self.__signal_id_4 = self.connect("drag-drop", self.__drag_drop_cb)
		self.__signal_id_5 = self.connect("drag-data-received", self.__drag_data_received_cb)
		self.__signal_id_6 = self.connect_after("populate-popup", self.__populate_popup_cb)
		self.__signal_id_7 = self.connect("copy-clipboard", self.__copy_clipboard_cb)
		self.__signal_id_8 = self.connect("cut-clipboard", self.__cut_clipboard_cb)
		self.__signal_id_9 = self.connect("paste-clipboard", self.__paste_clipboard_cb)
		self.__signal_id_11 = self.connect("button-press-event", self.__button_press_event_cb)
		self.__signal_id_12 = editor.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_13 = editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_14 = editor.connect("load-error", self.__load_error_cb)
		self.__signal_id_15 = editor.connect("enable-readonly", self.__enable_readonly_cb)
		self.__signal_id_16 = editor.connect("disable-readonly", self.__disable_readonly_cb)
		self.__signal_id_17 = editor.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_18 = editor.connect("hide-dialog", self.__hide_dialog_cb)
		self.__signal_id_19 = editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_20 = editor.connect("hide-bar", self.__hide_bar_cb)
		self.__signal_id_21 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_22 = editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_25 = editor.connect("reload-document", self.__reload_document_cb)
		# GConf notification monitors.
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__font_database_uri, MONITOR_FILE,
								self.__font_changed_cb)
		self.__client.notify_add("/apps/scribes/tab", self.__tab_width_cb)
		self.__client.notify_add("/apps/scribes/text_wrapping", self.__text_wrapping_cb)
		self.__client.notify_add("/apps/scribes/margin", self.__show_margin_cb)
		self.__client.notify_add("/apps/scribes/margin_position", self.__margin_position_cb)
		self.__client.notify_add("/apps/scribes/spell_check", self.__spell_check_cb)
		self.__client.notify_add("/apps/scribes/use_theme_colors", self.__themes_cb)
		self.__client.notify_add("/apps/scribes/fgcolor", self.__foreground_cb)
		self.__client.notify_add("/apps/scribes/bgcolor", self.__background_cb)
		self.__client.notify_add("/apps/scribes/use_tabs", self.__use_tabs_cb)
		self.__client.notify_add("/apps/scribes/SyntaxHighlight", self.__syntax_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the buffer container's attributes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__client = editor.gconf_client
		self.__editor = editor
		self.__registration_id = editor.register_object()
		self.__spell_checker = None
		self.__bar_is_visible = False
		self.__bar = None
		self.__scroll_id = None
		self.__move_id = None
		self.__monitor_id_1 = None
		# Path to the font database.
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		font_database_path = join(preference_folder, "Font.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__font_database_uri = get_uri_from_local_path(font_database_path)
		return

	def __set_properties(self):
		"""
		Set default properties.

		Much of the properties of the view can be defined by users. So the
		properties of the view are stored in GNOME's configuration database,
		GConf. During the text editor's initialization process,

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: Reference to the text editor instance.
		@type editor: An Editor object.
		"""
		# Drag and drop setup.
		targets = [("text/uri-list", 0, 80)]
		from gtk import DEST_DEFAULT_ALL
		from gtk.gdk import ACTION_COPY, BUTTON1_MASK, ACTION_DEFAULT
		self.drag_dest_set(DEST_DEFAULT_ALL, targets, ACTION_COPY)
		self.set_property("buffer", self.__editor.textbuffer)
		self.set_highlight_current_line(True)
		self.set_show_line_numbers(True)
		self.set_auto_indent(True)
		if self.__client.get("/apps/scribes/spell_check"):
			spell_check = self.__client.get_bool("/apps/scribes/spell_check")
			if spell_check:
				try:
					from gobject import GError
					from gtkspell import Spell
					from locale import getdefaultlocale
					self.__spell_checker = Spell(self, getdefaultlocale()[0])
				except GError:
					pass
		margin_position = 72
		if self.__client.get("/apps/scribes/margin_position"):
			margin_position = self.__client.get_int("/apps/scribes/margin_position")
		self.set_margin(margin_position)
		show_margin = False
		if self.__client.get("/apps/scribes/margin"):
			show_margin = self.__client.get_bool("/apps/scribes/margin")
		self.set_show_margin(show_margin)
		tab_width = 4
		if self.__client.get("/apps/scribes/tab"):
			tab_width = self.__client.get_int("/apps/scribes/tab")
		self.set_tabs_width(tab_width)
		use_tabs = True
		if self.__client.get("/apps/scribes/use_tabs"):
			use_tabs = self.__client.get_bool("/apps/scribes/use_tabs")
		self.set_insert_spaces_instead_of_tabs(not use_tabs)
		from FontMetadata import get_value
		font_name = get_value()
		from pango import FontDescription
		font = FontDescription(font_name)
		self.modify_font(font)
		wrap_mode_bool = True
		if self.__client.get("/apps/scribes/text_wrapping"):
			wrap_mode_bool = self.__client.get_bool("/apps/scribes/text_wrapping")
		use_theme_colors = True
		if self.__client.get("/apps/scribes/use_theme_colors"):
			use_theme_colors = self.__client.get_bool("/apps/scribes/use_theme_colors")
		from gtk import WRAP_WORD, WRAP_NONE
		if wrap_mode_bool:
			self.set_wrap_mode(WRAP_WORD)
		else:
			self.set_wrap_mode(WRAP_NONE)
		if use_theme_colors is False:
			# Use foreground and background colors specified by the user stored
			# in GConf, the GNOME configuration database.
			from gconf import VALUE_STRING
			fgcolor = "#000000"
			bgcolor = "#ffffff"
			if self.__client.get("/apps/scribes/fgcolor"):
				fgcolor = self.__client.get_string("/apps/scribes/fgcolor")
			if self.__client.get("/apps/scribes/bgcolor"):
				bgcolor = self.__client.get_string("/apps/scribes/bgcolor")
			try:
				from gtk.gdk import color_parse
				foreground_color = color_parse(fgcolor)
				background_color = color_parse(bgcolor)
			except TypeError:
				foreground_color = color_parse("#000000")
				background_color = color_parse("#ffffff")
			from gtk import STATE_NORMAL
			self.modify_base(STATE_NORMAL, background_color)
			self.modify_text(STATE_NORMAL, foreground_color)
		return

################################################################################
#
#						Signal and Event Handlers
#
################################################################################

	def __map_event_cb(self, widget, event):
		"""
		Handles callback when the textview widget is drawn to screen.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param widget: Reference to the text editor's buffer container.
		@type widget: A gtk.SourceView object.

		@param event: An event that occurs when the widgets are displayed on
			screen.
		@type event: A gtk.Event object.
		"""
		from gobject import idle_add
		idle_add(self.__refresh_view)
		return False

	def __drag_motion_cb(self, textview, context, x, y, time):
		"""
		Handles callback when a drag operation begins.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param textview: The text editor's view, or buffer container.
		@type textview: A gtk.SourceView object.

		@param context: The type of information being dragged.
		@type context: A gtk.Context object.

		@param x: The xcordinate of the cursor.
		@type x: An Integer object.

		@param y: The ycordinate of the cursor.
		@type y: An Integer object.

		@param time: The time the drag operation began.
		@type time: An Integer object.

		@return: False to propagate signals to parent widgets, True otherwise.
		@rtype: A Boolean object.
		"""
		from operator import contains
		if contains(context.targets, "text/uri-list"): return True
		return False

	def __drag_drop_cb(self, textview, context, x, y, time):
		"""
		Handles callback when a drop operation begins.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param textview: The text editor's view, or buffer container.
		@type textview: A gtk.SourceView object.

		@param context: The type of information being dragged.
		@type context: A gtk.Context object.

		@param x: The xcordinate of the cursor.
		@type x: An Integer object.

		@param y: The ycordinate of the cursor.
		@type y: An Integer object.

		@param time: The time the drag operation began.
		@type time: An Integer object.

		@return: False to propagate signals to parent widgets, True otherwise.
		@rtype: A Boolean object.
		"""
		from operator import contains
		if contains(context.targets, "text/uri-list"): return True
		return False

	def __drag_data_received_cb(self, textview, context, xcord, ycord,
								selection_data, info, timestamp):
		"""
		Handles callback when a drop operation finishes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param textview: The text editor's view, or buffer container.
		@type textview: A gtk.SourceView object.

		@param context: The type of information being dragged.
		@type context: A gtk.Context object.

		@param xcord: The xcordinate of the cursor.
		@type xcord: An Integer object.

		@param ycord: The ycordinate of the cursor.
		@type ycord: An Integer object.

		@param selection_data: A data selection
		@type selection_data: A gtk.Selection object.

		@param info: ?
		@type info: ? ? object.

		@param timestamp: The time the drag operation began.
		@type timestamp: An Integer object.

		@return: False to propagate signals to parent widgets, True otherwise.
		@rtype: A Boolean object.
		"""
		from operator import contains, not_, ne
		if not_(contains(context.targets, "text/uri-list")): return False
		if ne(info, 80): return False
		# Load file
		uri_list = list(selection_data.get_uris())
		self.__editor.instance_manager.open_files(uri_list)
		context.finish(True, False, timestamp)
		return True

	def __drag_data_get_cb(self, textview, context, data, info, time):
		"""
		Handles callback when the "drag-data-get" signal is emitted.

		@param self: Reference to the TemplateEditorDescriptionView instance.
		@type self: A TemplateEditorDescriptionView object.

		@param treeview: Reference to the TemplateEditorDescriptionView
		@type treeview: A TemplateEditorDescriptionView object.

		@param context: An object representing context data.
		@type context: A gtk.DragContext object.

		@param data: An object representing selection data.
		@type data: A gtk.SelectionData object.

		@param info: A unique identification number for the text editor.
		@type info: An Integer object.

		@param time: The time of the drag and drop operation.
		@type time: An Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		selection = self.get_buffer().get_selection_bounds()
		from operator import not_
		if not_(selection): return False
		string = self.get_buffer().get_text(selection[0], selection[1])
		data.set(data.target, 8, string)
		return False

	def __checking_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor is loading a document into the
		text editor's buffer.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("editable", False)
		self.set_property("highlight-current-line", False)
		self.set_property("cursor-visible", False)
		self.set_property("sensitive", False)
#		from gobject import idle_add
#		idle_add(self.__refresh_view)
		return False

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor has finished loading a document
		into the text editor's buffer.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		self.set_property("highlight-current-line", True)
		self.set_property("cursor-visible", True)
		self.set_property("editable", True)
		from gobject import idle_add
		idle_add(self.__refresh_view)
		return False

	def __reload_document_cb(self, *args):
		self.set_property("editable", False)
		return False

	def __load_error_cb(self, editor, uri):
		"""
		Handles callback when the text editor has finished loading a document
		into the text editor's buffer.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		self.set_property("cursor-visible", True)
		self.set_property("highlight-current-line", True)
		self.set_property("editable", True)
		from cursor import move_view_to_cursor
		move_view_to_cursor(self)
		return False

	def __enable_readonly_cb(self, editor):
		"""
		Handles callback when the text editor is switched to readonly mode.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("editable", False)
		self.set_property("highlight-current-line", False)
		self.set_property("cursor-visible", False)
		self.set_property("show-line-numbers", False)
#		from gobject import idle_add
#		idle_add(self.__refresh_view)
		return False

	def __disable_readonly_cb(self, editor):
		"""
		Handles callback when the text editor is switched from readonly to
		readwrite mode.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("editable", True)
		self.set_property("highlight-current-line", True)
		self.set_property("cursor-visible", True)
		self.set_property("show-line-numbers", True)
		from gobject import idle_add
		idle_add(self.__refresh_view)
		return False

	def __renamed_document_cb(self, editor, uri):
		"""
		Handles callback when the name of the document is renamed.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("cursor-visible", True)
		self.set_property("editable", True)
		self.set_property("highlight-current-line", True)
		self.set_property("cursor-visible", True)
		self.set_property("show-line-numbers", True)
		from gobject import idle_add
		idle_add(self.__refresh_view)
		return False

	def __show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's bar.
		@type bar: A ScribesBar object.
		"""
		self.__bar = bar
		self.__bar_is_visible = True
		self.set_property("editable", False)
		self.set_property("cursor-visible", False)
		self.set_property("accepts-tab", False)
		return False

	def __hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's bar.
		@type bar: A ScribesBar object.
		"""
		self.__bar_is_visible = False
		self.set_property("editable", True)
		self.set_property("cursor-visible", True)
		self.set_property("accepts-tab", True)
		from gobject import idle_add
		idle_add(self.__refresh_view)
		return False

	def __focus_in_event_cb(self, textview, event):
		"""
		Handles callback when the text editor's windows "focus-in-event" signal
		is emitted.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param window: The text editor's buffer container, or view.
		@type window: A ScribesTextView object.

		@param event: An event triggered when the text editor's window is focused.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if self.__bar_is_visible is False:
			self.grab_focus()
			#from gobject import idle_add
			#idle_add(self.__refresh_view)
		return False

	def __button_press_event_cb(self, textview, event):
		"""
		Handles callback when the "button-press-event" signal is emitted.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param textview: The text editor's view.
		@type textview: A ScribesTextView object.

		@param event: An event that occurs when the mouse buttons are pressed.
		@type event: A gtk.Event object.

		@param bar: The text editor's bar.
		@type bar: A ScribesBar object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if self.__bar_is_visible:
			self.__bar.hide_bar()
			return True
		return False

	def __populate_popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param textview: The text editor's buffer container.
		@type textview: A ScribesTextView object.

		@param menu: The text editor's popup menu.
		@type menu: A gtk.Menu object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import MenuItem, SeparatorMenuItem
		menu.insert(SeparatorMenuItem(), 0)
		return False

	def __hide_dialog_cb(self, *args):
		self.grab_focus()
		#from gobject import idle_add
		#idle_add(self.__refresh_view)
		return

	def __copy_clipboard_cb(self, textview):
		textbuffer = self.get_buffer()
		feedback = self.__editor.feedback
		# Get selection bounds
		selection = textbuffer.get_selection_bounds()

		# Depending on whether or not text is selected and copied, send appropriate
		# feedback back to the user via the statusbar.
		if selection:
			from internationalization import msg0089
			feedback.update_status_message(msg0089, "copy")
		else:
			from internationalization import msg0090
			feedback.update_status_message(msg0090, "fail")
		return False

	def __cut_clipboard_cb(self, textview):
		feedback = self.__editor.feedback
		if self.__editor.is_readonly:
			from internationalization import msg0145
			feedback.update_status_message(msg0145, "fail")
			return False
		textbuffer = self.get_buffer()

		# Get selection bounds
		selection = textbuffer.get_selection_bounds()
		# Depending on whether or not text is selected and copied, send appropriate
		# feedback back to the user via the statusbar.
		if selection:
			from internationalization import msg0091
			feedback.update_status_message(msg0091, "cut")
		else:
			from internationalization import msg0092
			feedback.update_status_message(msg0092, "fail")
		return False

	def __paste_clipboard_cb(self, textview):

		feedback = self.__editor.feedback
		if self.__editor.is_readonly:
			from internationalization import msg0145
			feedback.update_status_message(msg0145, "fail")
			return False
		# Check to see if there is text in the clipboard manager.
		from gtk import clipboard_get
		clipboard = clipboard_get()
		selection = clipboard.wait_for_text()

		# Depending on whether or not there is text in the clipboard manager, send
		# appropriate feedback back to the user via the statusbar.
		if selection:
			from internationalization import msg0093
			feedback.update_status_message(msg0093, "paste")
		else:
			from internationalization import msg0094
			feedback.update_status_message(msg0094, "fail")
		return False

	def __make_responsive(self):
		return False

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__destroy()
		return

################################################################################
#
#						GConf Notification Handlers
#
################################################################################

	def __font_changed_cb(self, *args):
		"""
		Handles callback when the font of the text editor changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.
		"""
		from pango import FontDescription
		from FontMetadata import get_value
		new_font = FontDescription(get_value())
		self.modify_font(new_font)
		return

	def __tab_width_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the tab width of the text editor changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		self.set_tabs_width(int(entry.value.to_string()))
		return

	def __text_wrapping_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the text wrapping mode of the text editor changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		from gtk import WRAP_NONE, WRAP_WORD
		if entry.value.get_bool():
			self.set_wrap_mode(WRAP_WORD)
		else:
			self.set_wrap_mode(WRAP_NONE)
		return

	def __margin_position_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the right margin position of the text editor
		changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		self.set_margin(int(entry.value.to_string()))
		return

	def __show_margin_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the right margin of the text editor is hidden or
		displayed.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		self.set_show_margin(entry.value.get_bool())
		return

	def __spell_check_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when spell checking is toggled on or off in the text
		editor.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.

		"""
		if entry.value.get_bool():
			from gobject import GError
			try:
				from gtkspell import Spell
				from locale import getdefaultlocale
				self.__spell_checker = Spell(self, getdefaultlocale()[0])
			except GError:
				pass
		else:
			self.__spell_checker.detach()
		return

	def __themes_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when of the text editor's view theme changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		# Set the foreground and background color of the text editor's buffer.
		if entry.value.get_bool():
			# Use foreground and background colors specified by the GTK+ theme.
			from gtk import RcStyle
			style = RcStyle()
			self.modify_style(style)
			#  Reset font to value in GConf
			value = client.get_string("/apps/scribes/font")
			from pango import FontDescription
			font = FontDescription(value)
			self.modify_font(font)
		else:
			try:
				# Use foreground and background colors specified by the
				# user stored in GConf, the GNOME configuration database.
				color = client.get_string("/apps/scribes/fgcolor")
				from gtk.gdk import color_parse
				foreground_color = color_parse(color)
				color = client.get_string("/apps/scribes/bgcolor")
				background_color = color_parse(color)
			except TypeError:
				foreground_color = color_parse("#000000")
				background_color = color_parse("#ffffff")
			from gtk import STATE_NORMAL
			self.modify_base(STATE_NORMAL, background_color)
			self.modify_text(STATE_NORMAL, foreground_color)
		return

	def __foreground_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the color text within the text editor changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		color = client.get_string("/apps/scribes/fgcolor")
		from gtk.gdk import color_parse
		foreground_color = color_parse(color)
		from gtk import STATE_NORMAL
		self.modify_text(STATE_NORMAL, foreground_color)
		from gobject import idle_add
		idle_add(self.__refresh_view)
		return

	def __background_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the background color of the text editor changes.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		color = client.get_string("/apps/scribes/bgcolor")
		from gtk.gdk import color_parse
		background_color = color_parse(color)
		from gtk import STATE_NORMAL
		self.modify_base(STATE_NORMAL, background_color)
		return

	def __use_tabs_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback #FIXME: yeap

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		use_tabs = client.get_bool("/apps/scribes/use_tabs")
		self.set_insert_spaces_instead_of_tabs(not use_tabs)
		return

	def __syntax_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback #FIXME: yeap

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		from syntax import activate_syntax_highlight
		from utils import get_language
		language = None
		if self.__editor.uri: language = get_language(self.__editor.uri)
		activate_syntax_highlight(self.get_buffer(), language)
		return

	def __refresh_view(self):
		"""
		Redraw elements of the view and its children.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.
		"""
		self.grab_focus()
#		self.__make_responsive()
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__refresh, priority=PRIORITY_LOW)
		return False

	def __refresh(self):
#		self.queue_draw()
#		self.queue_resize()
#		self.resize_children()
#		try:
#			self.window.process_updates(True)
#		except:
#			pass
#		self.__make_responsive()
		return False

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		self.__editor.disconnect_signal(self.__signal_id_5, self)
		self.__editor.disconnect_signal(self.__signal_id_6, self)
		self.__editor.disconnect_signal(self.__signal_id_7, self)
		self.__editor.disconnect_signal(self.__signal_id_8, self)
		self.__editor.disconnect_signal(self.__signal_id_9, self)
		self.__editor.disconnect_signal(self.__signal_id_11, self)
		self.__editor.disconnect_signal(self.__signal_id_12, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_13, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_14, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_15, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_16, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_17, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_18, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_19, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_20, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_21, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_22, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_25, self.__editor)
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		# Unregister object so that editor can quit.
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return
