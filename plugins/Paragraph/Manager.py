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
This module documents a class that implements paragraph operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class implements paragraph operations.
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
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__client = editor.gconf_client
		self.__buffer = editor.textbuffer
		self.__feedback = editor.feedback
		return

########################################################################
#
#							Public Methods
#
########################################################################

	def previous_paragraph(self):
		"""
		Move cursor to previous paragraph.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		cursor_iterator = self.__editor.get_cursor_iterator()
		current_line = cursor_iterator.get_line()
		from operator import eq, is_
		try:
			if eq(current_line, 0): raise RuntimeError
			line = self.__find_empty_line(cursor_iterator)
			if is_(line, None): raise ValueError
			self.__jump_to_line(line)
			from i18n import msg0003
			self.__feedback.update_status_message(msg0003, "yes", 5)
		except RuntimeError:
			from i18n import msg0004
			self.__feedback.update_status_message(msg0004, "warning", 5)
		except ValueError:
			self.__jump_to_line(0)
		return

	def next_paragraph(self):
		"""
		Move cursor to next paragraph.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		number_of_lines = self.__buffer.get_line_count()
		cursor_iterator = self.__editor.get_cursor_iterator()
		current_line = cursor_iterator.get_line()
		from operator import eq, is_
		try:
			if eq(current_line, number_of_lines-1): raise RuntimeError
			line = self.__find_empty_line(cursor_iterator, False)
			if is_(line, None): raise ValueError
			self.__jump_to_line(line)
			from i18n import msg0005
			self.__feedback.update_status_message(msg0005, "yes", 5)
		except RuntimeError:
			from i18n import msg0006
			self.__feedback.update_status_message(msg0006, "warning", 5)
		except ValueError:
			self.__jump_to_line(number_of_lines-1)
		return

	def select_paragraph(self):
		"""
		Select a paragraph.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		try:
			begin, end = self.__get_paragraph_position()
			self.__buffer.select_range(begin, end)
			from i18n import msg0007
			self.__feedback.update_status_message(msg0007, "yes", 5)
		except RuntimeError:
			from i18n import msg0001
			self.__feedback.update_status_message(msg0001, "warning", 5)
		return

	def reflow_paragraph(self):
		"""
		Reflow paragraph based on right margin position.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		if self.__is_readonly(): return
		try:
			start, end = self.__get_paragraph_position()
		except RuntimeError:
			from i18n import msg0001
			self.__feedback.update_status_message(msg0001, "warning", 5)
			return
		text = start.get_text(end)
		try:
			text = self.__reflow_text(text)
		except RuntimeError:
			from i18n import msg0002
			self.__feedback.update_status_message(msg0002, "warning", 5)
			return
		self.__buffer.begin_user_action()
		self.__buffer.delete(start, end)
		self.__buffer.insert_at_cursor(text)
		self.__buffer.end_user_action()
		from i18n import msg0009
		message = msg0009
		self.__feedback.update_status_message(message, "yes", 5)
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.delete_attributes(self)
		del self
		self = None
		return

################################################################################
#
#						Paragraph Helper Methods
#
################################################################################

	def __get_paragraph_position(self):
		"""
		Get start and end paragraph positions.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@return: The position of a paragraph.
		@rtype: A Tuple object.
		"""
		iterator = self.__get_current_line_iterator()
		if iterator.is_start() and iterator.is_end(): raise RuntimeError
		if self.__is_empty_line(iterator): raise RuntimeError
		first_paragraph_line = self.__find_empty_line(iterator)
		if first_paragraph_line is None:
			begin, end = self.__buffer.get_bounds()
		else:
			begin = self.__buffer.get_iter_at_line(first_paragraph_line)
			begin.forward_line()
		second_paragraph_line = self.__find_empty_line(iterator, False)
		if second_paragraph_line is None:
			start, end = self.__buffer.get_bounds()
		else:
			end = self.__buffer.get_iter_at_line(second_paragraph_line)
			end.backward_line()
			end.forward_to_line_end()
		return begin, end

	def __get_current_line_iterator(self):
		"""
		Get iterator at start of current line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@return: Return the iterator at start of current line.
		@rtype: A gtk.TextIter object.
		"""
		iterator = self.__editor.get_cursor_iterator()
		if iterator.starts_line(): return iterator
		line = iterator.get_line()
		return self.__buffer.get_iter_at_line(line)

	def __find_empty_line(self, iterator, backwards=True):
		"""
		Search backwards for empty lines.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param iterator: The cursor position
		@type iterator: A gtk.TextIter object.

		@return: Line number of empty line or None
		@rtype: An Integer or None object.
		"""
		from operator import not_
		while True:
			if backwards:
				if not_(iterator.backward_line()): return None
			else:
				if not_(iterator.forward_line()): return None
			if self.__is_empty_line(iterator): return iterator.get_line()
		return None

	def __is_empty_line(self, iterator):
		"""
		Whether or not a line is empty.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param iterator: Reference a position in the buffer.
		@type iterator: A gtk.TextIter object.

		@return: True if line is empty.
		@rtype: A Boolean object.
		"""
		if iterator.ends_line(): return True
		temporary_iterator = iterator.copy()
		temporary_iterator.forward_to_line_end()
		text = iterator.get_text(temporary_iterator)
		from operator import not_
		if not_(text): return True
		if text.isspace(): return True
		return False

	def __jump_to_line(self, line):
		"""
		Move cursor to a specific line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: Line to jump to.
		@type line: An Integer object.
		"""
		iterator = self.__buffer.get_iter_at_line(line)
		self.__buffer.place_cursor(iterator)
		from SCRIBES.cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		return

########################################################################
#
#					Paragraph Reflow Helper Methods
#
########################################################################

	def __reflow_text(self, text):
		"""
		Realign lines in text such that is line is not more than a
		specified character long.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param text: Text to reflow.
		@type text: A String object.

		@return: Realigned text.
		@rtype: A String object.
		"""
		from operator import not_, gt, le
		if not_(text) or text.isspace(): raise RuntimeError
		text_lines = text.split("\n")
		indentation = self.__get_indentation(text_lines[0])
		wrap_width = self.__calculate_wrap_width(indentation)
		reflowed_lines = []
		remainder = ""
		line = " ".join(text_lines)
		line = line.replace("\t", " ")
		line = line.strip()
		line = self.__respace_line(line)
		if gt(len(line), wrap_width):
			while True:
				new_line, remainder = self.__shorten_line(line, wrap_width)
				reflowed_lines.append(new_line)
				if le(len(remainder), wrap_width): break
				line = remainder.strip()
		else:
			reflowed_lines.append(line)
		if remainder: reflowed_lines.append(remainder)
		indented_reflowed_lines = self.__indent_lines(reflowed_lines, indentation)
		return "\n".join(indented_reflowed_lines)

	def __shorten_line(self, line, wrap_width):
		"""
		Shorten a line to a specified wrap width.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: Line to shorten.
		@type line: A String object.

		@param wrap_width: How long the line should be.
		@type wrap_width: An Integer object.

		@return: The shortened line and other strings that exceed the
			specified wrap width.
		@rtype: A Tuple object.
		"""
		from textwrap import wrap
		line = line.strip()
		new_lines = wrap(line, wrap_width, expand_tabs=False, replace_whitespace=False)
		new_line = new_lines[0]
		remainder = " ".join(new_lines[1:])
		return new_line.strip(), remainder.strip()

	def __indent_lines(self, reflowed_lines, indentation):
		"""
		Perform automatic indentation on each line, if necessary.

		Automatic indentation is based on the indentation of the first
		line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param reflowed_lines: Realigned lines for indentation.
		@type reflowed_lines: A List object.

		@return: A list of indented lines.
		@rtype: A List object.
		"""
		from operator import lt
		if lt(len(reflowed_lines), 2): return reflowed_lines
		indent_line = lambda x: indentation + x.strip()
		indented_lines = map(indent_line, reflowed_lines)
		return indented_lines

	def __get_indentation(self, line):
		"""
		Determine the indentation of a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: A line to check for indentation.
		@type line: A String object.
		"""
		indentation_list = []
		from operator import contains, not_
		for char in line:
			if not_(contains([" ", "\t"], char)): break
			indentation_list.append(char)
		return "".join(indentation_list)

	def __respace_line(self, line):
		"""
		Remove duplicate spaces in a line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param line: A line to remove duplicate spaces from.
		@type line: A String object.

		@return: A new line with single spaces.
		@rtype: A String object.
		"""
		line = line.split(" ")
		while True:
			try:
				line.remove("")
			except ValueError:
				break
		return " ".join(line)

	def __calculate_wrap_width(self, indentation):
		"""
		Determine wrap width.

		This function calculates the wrap width paying attention to
		automatic indentation.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param indentation: An indentation strings.
		@type indentation: A String object.

		@return: wrap width.
		@rtype: An Integer object.
		"""
		width = self.__get_right_margin_width()
		from operator import not_, ne
		if not_(indentation): return width
		tab_width = self.__get_tab_width()
		number_of_tab_chars = indentation.count("\t")
		number_of_space_chars = indentation.count(" ")
		width = width - (number_of_space_chars + (number_of_tab_chars * tab_width))
		return width

	def __get_tab_width(self):
		"""
		Get tab width from GConf.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@return: Tab width.
		@rtype: An Integer object.
		"""
		tab_width = 4
		if self.__client.get("/apps/scribes/tab"):
			tab_width = self.__client.get_int("/apps/scribes/tab")
		return tab_width

	def __is_readonly(self):
		"""
		Check if editor is in readonly mode.
		
		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		
		@return: True if editor is in readonly mode.
		@rtype: A Boolean object.
		"""
		from operator import not_
		if not_(self.__editor.is_readonly): return False
		from i18n import msg0010
		self.__editor.feedback.update_status_message(msg0010, "warning", 7)
		return True

	def __get_right_margin_width(self):
		"""
		Get margin or wrap width from Gconf.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@return: Margin/wrap width.
		@rtype: An Integer object.
		"""
		margin_position = 72
		if self.__client.get("/apps/scribes/margin_position"):
			margin_position = self.__client.get_int("/apps/scribes/margin_position")
		return margin_position

	def __precompile_methods(self):
		"""
		Optimize methods using Psyco.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		try:
			from psyco import bind
			bind(self.reflow_paragraph)
			bind(self.next_paragraph)
			bind(self.previous_paragraph)
			bind(self.select_paragraph)
			bind(self.__reflow_text)
			bind(self.__shorten_line)
			bind(self.__respace_line)
			bind(self.__indent_lines)
			bind(self.__calculate_wrap_width)
			bind(self.__get_paragraph_position)
			bind(self.__get_current_line_iterator)
			bind(self.__find_empty_line)
			bind(self.__is_empty_line)
			bind(self.__jump_to_line)
		except ImportError:
			pass
		return False
