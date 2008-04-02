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
This module documents a class that (un)comments lines in several source
code

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class (un)comments lines in several source code.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__has_selection = False
		self.__commented = False
		self.__readonly = False
		iterator = editor.get_cursor_iterator()
		self.__selection_begin_index = None
		self.__selection_begin_line = None
		self.__selection_end_index = None
		self.__selection_end_line = None
		return

	def __backward_to_line_begin(self, iterator):
		"""
		Move an iterator to the beginning of a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param iterator: An iterator.
		@type iterator: A gtk.Iter object.
		"""
		if iterator.starts_line(): return iterator
		while True:
			iterator.backward_char()
			if iterator.starts_line(): break
		return iterator

	def __forward_to_line_end(self, iterator):
		"""
		Move an iterator to the end of a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param iterator: An object that represents a position in a buffer.
		@type iterator: A gtk.Iter object.
		"""
		if iterator.ends_line(): return iterator
		iterator.forward_to_line_end()
		return iterator

	def __get_selection_range(self):
		"""
		Get the range of a selection.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__has_selection = True
		begin, end = self.__buffer.get_selection_bounds()
		self.__selection_begin_index = begin.get_line_index()
		self.__selection_begin_line = begin.get_line()
		self.__selection_end_index = end.get_line_index()
		self.__selection_end_line = end.get_line()
		end_position = self.__forward_to_line_end(end)
		begin_position = self.__backward_to_line_begin(begin)
		return begin_position, end_position

	def __get_range(self):
		"""
		Get the range of a line or selection of lines to comment.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		if self.__buffer.get_property("has-selection"): return self.__get_selection_range()
		iterator = self.__editor.get_cursor_iterator()
		if iterator.starts_line() and iterator.ends_line(): return None
		end_position = self.__forward_to_line_end(iterator.copy())
		begin_position = self.__backward_to_line_begin(iterator)
		return begin_position, end_position

	def __get_first_nonwhitespace(self, string):
		"""
		Get the first non-white space character in a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param string: A string.
		@type string: A String object.
		"""
		if not string: return None
		string = string.strip(" \t")
		if not string: return None
		return string[0]

	def __line_is_comment(self, line):
		"""
		Check if a line is a comment.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: A text on a line.
		@type line: A String object.
		"""
		is_comment = True if self.__get_first_nonwhitespace(line) == "#" else False
		return is_comment

	def __should_comment(self, lines):
		"""
		Check whether or not line(s) should be commented.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param lines: A group of lines
		@type lines: A List object.
		"""
		should_comment = True
		for line in lines:
			if self.__line_is_comment(line) is False: continue
			should_comment = False
			break
		return should_comment

	def __comment_line(self, line):
		"""
		Comment a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: A line to be commented.
		@type line: A String object.
		"""
		if self.__line_is_comment(line): return line
		line = "#" + line
		return line

	def __uncomment_line(self, line):
		"""
		Uncomment a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: A line to be uncommented.
		@type line: A String object.
		"""
		while self.__line_is_comment(line):
			line = line.replace("#", "", 1)
		return line

	def __comment_lines(self, lines):
		"""
		Comment a group of lines.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param lines: A group of lines
		@type lines: A List object.
		"""
		lines = map(self.__comment_line, lines)
		return lines

	def __uncomment_lines(self, lines):
		"""
		Uncomment a group of lines.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param lines: A group of lines
		@type lines: A List object.
		"""
		lines = map(self.__uncomment_line, lines)
		return lines

	def __update_feedback_message(self):
		"""
		Send feedback message to the status area.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		if self.__readonly:
			from i18n import msg5
			message = msg5
			self.__editor.feedback.update_status_message(message, "no", 5)
		else:
			if self.__commented:
				if self.__has_selection:
					from i18n import msg1
					message = msg1
				else:
					line = self.__editor.get_cursor_iterator().get_line() + 1
					from i18n import msg2
					message = msg2 % line
			else:
				if self.__has_selection:
					from i18n import msg3
					message = msg3
				else:
					line = self.__editor.get_cursor_iterator().get_line() + 1
					from i18n import msg4
					message = msg4 % line
			self.__editor.feedback.update_status_message(message, "yes", 5)
		return

	def __reset_flags(self):
		"""
		Reset flags.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__has_selection = False
		self.__commented = False
		self.__readonly = False
		return

	def toggle_comment(self):
		"""
		(Un)comment lines in python source code.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		try:
			from Exceptions import ReadOnlyError
			if self.__editor.is_readonly: raise ReadOnlyError
			offset = self.__editor.get_cursor_iterator().get_offset()
			begin, end = self.__get_range()
			text = self.__buffer.get_text(begin, end)
			lines = text.split("\n")
			if self.__should_comment(lines):
				self.__commented = True
				lines = self.__comment_lines(lines)
				offset += 1
			else:
				self.__commented = False
				lines = self.__uncomment_lines(lines)
				# If line is not empty (offset - 1)
				if not (len(lines) == 1 and not lines[0]): offset -= 1
			text = "\n".join(lines)
			self.__buffer.place_cursor(begin)
			self.__buffer.delete(begin, end)
			self.__buffer.insert_at_cursor(text)
			if self.__has_selection:
				begin = self.__get_begin_selection()
				end = self.__get_end_selection()
				self.__buffer.select_range(begin, end)
			else:
				iterator = self.__buffer.get_iter_at_offset(offset)
				self.__buffer.place_cursor(iterator)
		except TypeError:
			self.__buffer.insert_at_cursor("#")
			self.__commented = True
			iterator = self.__buffer.get_iter_at_offset(offset)
			self.__buffer.place_cursor(iterator)
		except ReadOnlyError:
			self.__readonly = True
		finally:
			self.__update_feedback_message()
			self.__reset_flags()
		return

	def __get_begin_selection(self):
		iterator = self.__buffer.get_iter_at_line(self.__selection_begin_line)
		line_size = iterator.get_bytes_in_line()
		if self.__selection_begin_index >= line_size:
			begin = self.__forward_to_line_end(iterator)
			begin.forward_char()
		else:
			begin = self.__buffer.get_iter_at_line_index(self.__selection_begin_line, self.__selection_begin_index)
		if self.__commented:
			begin.forward_char()
		else:
			begin.backward_char()
		return begin

	def __get_end_selection(self):
		iterator = self.__buffer.get_iter_at_line(self.__selection_end_line)
		line_size = iterator.get_bytes_in_line()
		if self.__selection_end_index >= line_size:
			end = self.__forward_to_line_end(iterator)
			end.forward_char()
		else:
			end = self.__buffer.get_iter_at_line_index(self.__selection_end_line, self.__selection_end_index)
		if self.__commented:
			end.forward_char()
		else:
			end.backward_char()
		return end

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		del self
		self = None
		return
