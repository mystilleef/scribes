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

from gtksourceview2 import View, Buffer

class Editor(View):
	"""
	This class defines the behavior of the add/edit dialog editor.
	"""

	def __init__(self, manager, editor):
		View.__init__(self, Buffer())
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = self.__buffer.connect("notify::cursor-position", self.__cursor_position_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("language-selected", self.__language_selected_cb)
		self.__sigid4 = self.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid5 = self.__buffer.connect_after("insert-text", self.__insert_text_cb)
		self.__sigid6 = manager.connect("dialog-hide-window", self.__hide_cb)
		self.__sigid7 = manager.connect("show-edit-dialog", self.__show_edit_dialog_cb)
		self.__sigid8 = manager.connect("valid-trigger", self.__valid_trigger_cb)
		self.__sigid9 = manager.connect("temp-selected", self.__temp_selected_cb)
		self.__sigid10 = manager.connect("process-2", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = self.get_property("buffer")
		self.__tag = self.__create_tag()
		self.__variable_region = None
		self.__markers = None
		self.__template = ""
		self.__placeholder_region = None
		self.__language = None
		return

	def __set_properties(self):
		scroll = self.__manager.dglade.get_widget("ScrollWin")
		scroll.add(self)
		self.set_property("auto-indent", True)
		self.set_property("show-line-numbers", False)
		self.set_property("show-right-margin", False)
		self.__buffer.set_highlight_syntax(False)
#		self.__buffer.set_property("check-brackets", False)
		scheme = self.__buffer.get_style_scheme()
		self.__buffer.set_style_scheme(scheme)
		self.set_property("cursor-visible", True)
		self.set_property("editable", True)
		self.set_property("sensitive", False)
		value = self.__editor.textview.get_tab_width()
		self.set_tab_width(value)
		self.set_indent_width(-1)
		value = self.__editor.textview.get_insert_spaces_instead_of_tabs()
		self.set_insert_spaces_instead_of_tabs(value)
		value = self.__editor.textview.get_pango_context().get_font_description()
		self.modify_font(value)
		value = self.__editor.textview.get_wrap_mode()
		self.set_wrap_mode(value)
		return

	def __create_tag(self):
		tag = self.__buffer.create_tag()
		tag.set_property("background", "#ADD8E6")
		tag.set_property("foreground", "white")
		return tag

	def __update_template_database(self, data):
		name, description = data
		start, end = self.__buffer.get_bounds()
		template = self.__buffer.get_text(start, end)
		key = self.__language + "|" + name
		data = description, template
		from Metadata import set_value
		set_value(key, data)
		return False

	def __activate_syntax_highlight(self, language_id):
		self.__buffer.set_highlight_syntax(False)
		language = self.__editor.language_manager.get_language(language_id)
		if not language: return False
		self.__buffer.set_language(language)
		self.__buffer.set_highlight_syntax(True)
		return False

	def __analyze_input(self, keyval):
		result = False
		from gtk import keysyms
		if (keyval == keysyms.dollar):
			self.__process_dollar_character()
			result = True
		elif (keyval == keysyms.braceleft):
			result = self.__process_braceleft_character()
		elif (keyval == keysyms.braceright):
			result = self.__process_braceright_character()
		return result

	def __process_dollar_character(self):
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
		text = self.__buffer.get_text(selection[0], selection[1])
		self.__buffer.delete(selection[0], selection[1])
		string = "${" + text + "}"
		self.__buffer.insert_at_cursor(string)
		return

	def __process_braceleft_character(self):
		if not (self.__placeholder_region): return False
		return True

	def __process_braceright_character(self):
		if not (self.__placeholder_region): return False
		iterator = self.__buffer.get_iter_at_mark(self.__placeholder_region[1])
		self.__buffer.place_cursor(iterator)
		return True

	def __clear_tags_and_marks(self):
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
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id3)
		except AttributeError:
			pass
		self.__language = language
		self.__id3 = idle_add(self.__activate_syntax_highlight, language, priority=9999)
		return False

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, manager)
		self.__editor.disconnect_signal(self.__sigid4, self)
		self.__editor.disconnect_signal(self.__sigid5, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid6, manager)
		self.__editor.disconnect_signal(self.__sigid7, manager)
		self.__editor.disconnect_signal(self.__sigid8, manager)
		self.__editor.disconnect_signal(self.__sigid9, manager)
		self.__editor.disconnect_signal(self.__sigid10, manager)
		self.destroy()
		self = None
		del self
		return

	def __cursor_position_cb(self, *args):
		if not (self.__placeholder_region): return
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
		if not (self.__placeholder_region): return False
		begin = self.__buffer.get_iter_at_mark(self.__variable_region[0])
		end = self.__buffer.get_iter_at_mark(self.__variable_region[1])
		self.__buffer.apply_tag(self.__tag, begin, end)
		return False

	def __hide_cb(self, *args):
		self.__clear_tags_and_marks()
		self.__buffer.set_text("")
		return

	def __show_edit_dialog_cb(self, *args):
		self.__buffer.set_text(self.__template)
		return False

	def __valid_trigger_cb(self, manager, sensitive):
		self.set_property("sensitive", sensitive)
		return False

	def __temp_selected_cb(self, manager, template):
		self.__template = template
		return False

	def __process_cb(self, manager, data):
		self.__update_template_database(data)
		self.__manager.emit("dialog-hide-window")
		return False
