# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This module documents a class that implements smart indentation for
Python source code.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class implements smart indentation for Python source code.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sig_id1 = self.__textview.connect('key-press-event', self.__key_press_event_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__textview = editor.textview
		return

	def __backward_to_line_begin(self, iterator):
		if iterator.starts_line(): return iterator
		while True:
			iterator.backward_char()
			if iterator.starts_line(): break
		return iterator

	def __forward_to_line_end(self, iterator):
		if iterator.ends_line(): return iterator
		iterator.forward_to_line_end()
		return iterator

	def __get_line_text(self):
		iterator = self.__editor.get_cursor_position()
		begin = self.__backward_to_line_begin(iterator.copy())
		end = self.__forward_to_line_end(iterator)
		text = self.__editor.textbuffer.get_text(begin, end)
		return text

	def __line_ends_with_colon(self):
		line_text = self.__get_line_text().strip(" \t")
		value = True if line_text.endswith(":") else False
		return value

	def __get_line_indentation(self):
		iterator = self.__editor.get_cursor_iterator()
		begin = self.__backward_to_line_begin(iterator)
		iterator = begin.copy()
		while True:
			if not (begin.get_char() in (" ", "\t")): break
			begin.forward_char()
		whitespaces = self.__editor.textbuffer.get_text(iterator, begin)
		return whitespaces

	def __get_indentation_for_next_line(self):
		whitespaces = self.__get_line_indentation()
		indentation_width = self.__textview.get_tab_width()
		if not whitespaces:
			if self.__textview.get_insert_spaces_instead_of_tabs():
				whitespaces = " " * indentation_width
			else:
				whitespaces = "\t"
		else:
			whitespaces = whitespaces.replace("\t", " " * indentation_width)
			number = whitespaces.count(" ")
			number_of_indentation_spaces = number - (number % indentation_width)
			if self.__textview.get_insert_spaces_instead_of_tabs():
				whitespaces = " " * (number_of_indentation_spaces + indentation_width)
			else:
				whitespaces = "\t" * ((number_of_indentation_spaces / indentation_width) + 1)
		return whitespaces

	def __get_dedentation_for_next_line(self):
		whitespaces = self.__get_line_indentation()
		indentation_width = self.__textview.get_tab_width()
		if not whitespaces: return ""
		whitespaces = whitespaces.replace("\t", " " * indentation_width)
		number = whitespaces.count(" ")
		number_of_indentation_spaces = number - (number % indentation_width)
		if self.__textview.get_insert_spaces_instead_of_tabs():
			whitespaces = " " * number_of_indentation_spaces
			if indentation_width == whitespaces.count(" "): return ""
			whitespaces = whitespaces[:indentation_width]
		else:
			whitespaces = "\t" * ((number_of_indentation_spaces / indentation_width) - 1)
		return whitespaces

	def __insert_indentation_on_next_line(self, whitespaces):
		iterator = self.__editor.get_cursor_iterator()
		iterator = self.__forward_to_line_end(iterator)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.textbuffer.insert_at_cursor("\n" + whitespaces)
		return

	def __indent_next_line(self):
		whitespaces = self.__get_indentation_for_next_line()
		self.__insert_indentation_on_next_line(whitespaces)
		return

	def __dedent_next_line(self):
		whitespaces = self.__get_dedentation_for_next_line()
		self.__insert_indentation_on_next_line(whitespaces)
		return

	def __cursor_is_before_colon(self):
		iterator = self.__editor.get_cursor_iterator()
		end = self.__forward_to_line_end(iterator.copy())
		from gtk import TEXT_SEARCH_TEXT_ONLY
		if iterator.forward_search(":", TEXT_SEARCH_TEXT_ONLY ,end): return True
		return False

	def __cursor_is_before_return(self):
		iterator = self.__editor.get_cursor_iterator()
		end = self.__editor.forward_to_line_end(iterator.copy())
		text = self.__editor.textbuffer.get_text(iterator, end).strip(" \t")
		if text: return True
		return False

	def __starts_with_return(self):
		text = self.__get_line_text()
		text = text.strip(" \t")
		if text.startswith("return"): return True
		return False

	def __key_press_event_cb(self, textview, event):
		from gtk.keysyms import Return
		if event.keyval != Return: return False
		ends_with_colon = self.__line_ends_with_colon()
		if ends_with_colon:
			if self.__cursor_is_before_colon(): return False
			self.__indent_next_line()
			return True
		starts_with_return = self.__starts_with_return()
		if not starts_with_return: return False
		if self.__cursor_is_before_return(): return False
		self.__dedent_next_line()
		return True

	def destroy(self):
		self.__editor.disconnect_signal(self.__sig_id1, self.__textview)
		del self
		self = None
		return
