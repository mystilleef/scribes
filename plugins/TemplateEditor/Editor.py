# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that defines the behavior of the editor
in the add or edit dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import SIGNAL_RUN_LAST, TYPE_NONE
from gtksourceview import SourceView, SourceBuffer

class Editor(SourceView):
	"""
	This class defines the behavior of the add/edit dialog editor.
	"""

	def __init__(self, manager, editor, language):
		"""
		Initialize object.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param language: A language category.
		@type language: A String object.
		"""
		SourceView.__init__(self, SourceBuffer())
		self.__init_attributes(manager, editor, language)
		self.__set_properties()
		self.__activate_syntax_highlight(language)
		self.__signal_id_1 = self.__buffer.connect("notify::cursor-position", self.__cursor_position_cb)
		self.__signal_id_2 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_3 = manager.connect("language-selected", self.__language_selected_cb)
		self.__signal_id_4 = self.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_5 = self.__buffer.connect_after("insert-text", self.__insert_text_cb)
		self.__signal_id_6 = manager.connect("hide", self.__hide_cb)

	def __init_attributes(self, manager, editor, language):
		"""
		Initialize data attributes.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param language: A language category.
		@type language: A String object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__buffer = self.get_property("buffer")
		self.__tag = self.__create_tag()
		self.__client = editor.gconf_client
		self.__variable_region = None
		self.__markers = None
		self.__placeholder_region = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.
		"""
		self.__buffer.set_property("highlight", False)
		self.__buffer.set_property("check-brackets", True)
		self.__buffer.notify("cursor-position")
		self.set_property("auto-indent", True)
		self.set_property("show-line-markers", False)
		self.set_property("show-line-numbers", False)
		self.set_property("show-margin", False)
		self.set_property("cursor-visible", True)
		self.set_property("editable", True)
		self.set_property("sensitive", False)
		from SCRIBES.MarginPositionMetadata import get_value
		margin_position = get_value()
		self.set_margin(margin_position)
		from SCRIBES.DisplayRightMarginMetadata import get_value
		show_margin = get_value()
		self.set_show_margin(show_margin)
		from SCRIBES.TabWidthMetadata import get_value
		tab_width = get_value()
		self.set_tabs_width(tab_width)
		from SCRIBES.UseTabsMetadata import get_value
		use_tabs = get_value()
		self.set_insert_spaces_instead_of_tabs(not use_tabs)
		from SCRIBES.FontMetadata import get_value
		font_name = get_value()
		from pango import FontDescription
		font = FontDescription(font_name)
		self.modify_font(font)
		from gtk import WRAP_WORD, WRAP_NONE
		from SCRIBES.TextWrappingMetadata import get_value
		wrap_mode_bool = get_value()
		if wrap_mode_bool:
			self.set_wrap_mode(WRAP_WORD)
		else:
			self.set_wrap_mode(WRAP_NONE)
		from SCRIBES.UseThemeMetadata import get_value
		use_theme_colors = get_value()
		if use_theme_colors is False:
			from SCRIBES.ForegroundColorMetadata import get_value
			fgcolor = get_value()
			from SCRIBES.BackgroundColorMetadata import get_value
			bgcolor = get_value()
			from gtk.gdk import color_parse
			foreground_color = color_parse(fgcolor)
			background_color = color_parse(bgcolor)
			from gtk import STATE_NORMAL
			self.modify_base(STATE_NORMAL, background_color)
			self.modify_text(STATE_NORMAL, foreground_color)
		return

	def __create_tag(self):
		"""
		Create a tag for the placeholder.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.
		"""
		tag = self.__buffer.create_tag()
		tag.set_property("background", "#ADD8E6")
		return tag

	def __activate_syntax_highlight(self, language_id):
		"""
		Toggle syntax highlight on for a particular language.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param language_id: An identification for a particular language.
		@type language_id: A String object.
		"""
		self.__buffer.set_property("highlight", True)
		from gtksourceview import SourceLanguage, SourceLanguagesManager
		manager = SourceLanguagesManager()
		languages = manager.get_available_languages()
		from operator import eq
		for language in languages:
			if eq(language.get_id(), language_id): break
		from SCRIBES.syntax import activate_syntax_highlight
		activate_syntax_highlight(self.__buffer, language)
		return

	def __analyze_input(self, keyval):
		result = False
		from operator import eq
		from gtk import keysyms
		if eq(keyval, keysyms.dollar):
			self.__process_dollar_character()
			result = True
		elif eq(keyval, keysyms.braceleft):
			result = self.__process_braceleft_character()
		elif eq(keyval, keysyms.braceright):
			result = self.__process_braceright_character()
		return result

	def __process_dollar_character(self):
		"""
		Insert placeholder into the editor's buffer.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param keyval: A value representing a keyboard characters.
		@type keyval: An Integer object.
		"""
		if self.__placeholder_region: return
		selection = self.__buffer.get_selection_bounds()
		if selection:
			self.__enclose_selection(selection)
			return
		from SCRIBES.cursor import get_cursor_iterator
		iterator = get_cursor_iterator(self.__buffer)
		first_mark = self.__buffer.create_mark(None, iterator, True)
		self.__buffer.insert_at_cursor("${placeholder}")
		iterator = get_cursor_iterator(self.__buffer)
		last_mark = self.__buffer.create_mark(None, iterator, False)
		iterator = self.__buffer.get_iter_at_mark(first_mark)
		iterator.forward_chars(2)
		second_mark = self.__buffer.create_mark(None, iterator, True)
		iterator = self.__buffer.get_iter_at_mark(last_mark)
		iterator.backward_char()
		third_mark = self.__buffer.create_mark(None, iterator, False)
		self.__variable_region = second_mark, third_mark
		self.__placeholder_region = first_mark, last_mark
		self.__markers = [first_mark, second_mark, third_mark, last_mark]
		begin = self.__buffer.get_iter_at_mark(second_mark)
		end = self.__buffer.get_iter_at_mark(third_mark)
		self.__buffer.select_range(begin, end)
		return

	def __enclose_selection(self, selection):
		"""
		Enclose selected text in placeholders.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param selection: The position of selected text in buffer.
		@type selection: A Tuple object.
		"""
		text = self.__buffer.get_text(selection[0], selection[1])
		self.__buffer.delete(selection[0], selection[1])
		string = "${" + text + "}"
		self.__buffer.insert_at_cursor(string)
		return

	def __process_braceleft_character(self):
		"""
		Prevent insertion of the opening parenthesis if the cursor is
		within the a placeholder region.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param keyval: A value representing a keyboard characters.
		@type keyval: An Integer object.
		"""
		from operator import not_
		if not_(self.__placeholder_region): return False
		return True

	def __process_braceright_character(self):
		"""
		Move the cursor to the end of the placeholder region if the
		cursor is within the placeholder region.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param keyval: A value representing a keyboard characters.
		@type keyval: An Integer object.
		"""
		from operator import not_
		if not_(self.__placeholder_region): return False
		iterator = self.__buffer.get_iter_at_mark(self.__placeholder_region[1])
		self.__buffer.place_cursor(iterator)
		return True

	def __clear_tags_and_marks(self):
		"""
		Remove tags and marks from the textbuffer.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.
		"""
		self.__placeholder_region = None
		self.__variable_region = None
		if self.__markers:
			for mark in self.__markers:
				if mark.get_deleted() is False:
					self.__buffer.delete_mark(mark)
		self.__markers = None
		begin, end = self.__buffer.get_bounds()
		self.__buffer.remove_tag(self.__tag, begin, end)
		return

	def __language_selected_cb(self, manager, language):
		"""
		Handles callback when the "language-selected" signal is emitted.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param manager: Reference to the TemplateManager
		@type manager: A TemplateManager object.

		@param language: A language.
		@type language: A String object.
		"""
		from operator import eq
		if eq(language, "General"):
			self.__buffer.set_property("highlight", False)
		else:
			self.__activate_syntax_highlight(language)
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param manager: Reference to the TemplateManager
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__buffer)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__buffer)
		self.__editor.disconnect_signal(self.__signal_id_6, manager)
		self.destroy()
		self = None
		del self
		return

	def __cursor_position_cb(self, *args):
		"""
		Handles callback when the "cursor-position" signal is emitted.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.
		"""
		from operator import not_
		if not_(self.__placeholder_region): return
		begin = self.__buffer.get_iter_at_mark(self.__placeholder_region[0])
		end = self.__buffer.get_iter_at_mark(self.__placeholder_region[1])
		from SCRIBES.cursor import get_cursor_iterator
		iterator = get_cursor_iterator(self.__buffer)
		if iterator.in_range(begin, end): return
		self.__clear_tags_and_marks()
		return

	def __key_press_event_cb(self, textview, event):
		return self.__analyze_input(event.keyval)

	def __insert_text_cb(self, textbuffer, iterator, text, length):
		"""
		Handles callback when the "insert-text" signal is emitted.

		@param self: Reference to the Editor instance.
		@type self: A Editor object.

		@param textbuffer: The buffer for the dialog.
		@type textbuffer: A SourceBuffer object.

		@param iterator: The position where text is to be inserted.
		@type iterator: A gtk.TextIter object.

		@param text: The text to be inserted into the buffer.
		@type text: A String object.

		@param length: The length of text to be inserted into the buffer.
		@type length: An Integer object.
		"""
		from operator import not_
		if not_(self.__placeholder_region): return False
		begin = self.__buffer.get_iter_at_mark(self.__variable_region[0])
		end = self.__buffer.get_iter_at_mark(self.__variable_region[1])
		self.__buffer.apply_tag(self.__tag, begin, end)
		return False

	def __hide_cb(self, *args):
		"""
		Handles callback when the "hide" signal is emitted.

		@param self: Reference to the Editor instance.
		@type self: An Editor object.
		"""
		self.__clear_tags_and_marks()
		return
