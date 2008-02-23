# -*- coding: utf-8 -*-
# Copyright (c) 2005 Lateef Alabi-Oki
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
This module documents functions that implement line operations in
gtk.TextBuffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright (c) 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

newlines = ["\n", "\x00", "\r\n", "\x0D\x0A", "\r"]

def duplicate_line(textbuffer):
	"""
	Duplicate line or selected lines.

	@param textbuffer: Reference to a buffer.
	@type textbuffer: A gtk.TextBuffer object.
	"""
	from SCRIBES.cursor import get_cursor_iterator
	iterator = get_cursor_iterator(textbuffer)
	cursor_offset = iterator.get_line_offset()
	start, end = __get_boundaries(textbuffer)
	end_offset = end.get_offset()
	text = "\n" + textbuffer.get_text(start, end)
	textbuffer.begin_user_action()
	textbuffer.insert(end, text)
	textbuffer.end_user_action()
	iterator = textbuffer.get_iter_at_offset(end_offset)
	iterator.forward_line()
	iterator.set_line_offset(cursor_offset)
	textbuffer.place_cursor(iterator)
	return

def __get_boundaries(textbuffer):
	"""
	Get start and end of a line or selection.

	@param textbuffer: Reference to a buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Start and end of line(s) to be copied.
	@rtype: A Tuple object.
	"""
	if textbuffer.get_has_selection():
		start, end = textbuffer.get_selection_bounds()
	else:
		from SCRIBES.cursor import get_cursor_iterator
		start = get_cursor_iterator(textbuffer)
		end = start.copy()
	__backward_to_line_start(start)
	__forward_to_line_end(end)
	return start, end

def __backward_to_line_start(iterator):
	while True:
		if iterator.starts_line(): return
		iterator.backward_char()
	return

def __forward_to_line_end(iterator):
	if iterator.ends_line(): return
	iterator.forward_to_line_end()
	return

def get_line_bounds(textbuffer):
	"""
	Get the beginning and end position of a line in a gtk.TextBuffer.

	@param textbuffer: The textbuffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: The beginning and end position of a line.
	@rtype: A Tuple object containing a pair of gtk.TextIter.
	"""
	from SCRIBES.cursor import get_cursor_line
	selection_bound = textbuffer.get_selection_bounds()
	if selection_bound:
		iterator = selection_bound[1]
		last_line = iterator.get_line()
		begin_position = textbuffer.get_iter_at_line(last_line)
		end_position = iterator.copy()
		if not_(iterator.ends_line()): end_position.forward_to_line_end()
	else:
		cursor_line = get_cursor_line(textbuffer)
		begin_position = textbuffer.get_iter_at_line(cursor_line)
		end_position = begin_position.copy()
		end_position.forward_to_line_end()
	return begin_position, end_position

def get_text_on_line(textbuffer, line):
	"""
	Get the text on a line in the editor's buffer.

	@param line: A line in the text editor's buffer.
	@type line: An Integer object.

	@param text: The text on a line in the buffer.
	@type text: A String object.
	"""
	begin_position = textbuffer.get_iter_at_line(line)
	if begin_position.ends_line(): return ""
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	text = textbuffer.get_text(begin_position, end_position)
	return text

def select_line(textbuffer):
	"""
	Select the current line in a gtk.TextBuffer.

	The current line is the line the cursor is on.

	@param textbuffer: The textbuffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Return True if the operation is successful.
	@rtype: A Boolean object.
	"""
	begin_position, end_position = get_line_bounds(textbuffer)
	if begin_position.ends_line(): return False
	textbuffer.select_range(begin_position, end_position)
	return True

def delete_line(textbuffer):
	textbuffer.begin_user_action()
	try:
		begin_position, end_position = get_line_bounds(textbuffer)
		start_position = begin_position.copy()
		begin_position, end_position = __get_end_line_position(begin_position)
		textbuffer.delete(start_position, end_position)
	except TypeError:
		try:
			__delete_last_line(textbuffer)
		except TypeError:
			pass
	textbuffer.end_user_action()
	return

def __delete_last_line(textbuffer):
	begin_position, end_position = get_line_bounds(textbuffer)
	if begin_position.ends_line():
		begin_position.backward_line()
		begin_position, end_position = __get_end_line_position(begin_position)
		textbuffer.delete(begin_position, end_position)
	else:
		textbuffer.delete(begin_position, end_position)
		from SCRIBES.cursor import get_cursor_iterator
		iterator = get_cursor_iterator(textbuffer)
		iterator.backward_line()
		start_position, end_position = __get_end_line_position(iterator)
		textbuffer.delete(start_position, end_position)
	return

def __get_end_line_position(iterator):
	from gtk import TEXT_SEARCH_VISIBLE_ONLY, TEXT_SEARCH_TEXT_ONLY
	for endline in newlines:
		try:
			begin_position, end_position = iterator.forward_search(endline, TEXT_SEARCH_TEXT_ONLY)
			return begin_position, end_position
		except TypeError:
			continue
	return None

def join_line(textbuffer):
	"""
	Join next line in the buffer to the current one.

	@param textbuffer: The text buffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Return True if the operation is successful.
	@rtype: A Boolean object.
	"""
	try:
		mark = None
		begin_position, end_position = get_line_bounds(textbuffer)
		from gtk import TEXT_SEARCH_VISIBLE_ONLY
		begin_match, end_match = begin_position.forward_search("\n", TEXT_SEARCH_VISIBLE_ONLY)
		mark = textbuffer.create_mark(None, begin_match, True)
		textbuffer.begin_user_action()
		textbuffer.delete(begin_match, end_match)
		begin_position = textbuffer.get_iter_at_mark(mark)
		end_position = begin_position.copy()
		if begin_position.backward_char():
			while begin_position.get_char() in [" ", "\t"]:
				begin_position.backward_char()
			begin_position.forward_char()
		while end_position.get_char() in [" ", "\t"]:
			end_position.forward_char()
		textbuffer.delete(begin_position, end_position)
		begin_position = textbuffer.get_iter_at_mark(mark)
		textbuffer.insert(begin_position, " ")
		if mark.get_deleted() is False:
			textbuffer.delete_mark(mark)
		textbuffer.end_user_action()
	except TypeError:
		if mark is None:
			return False
		if mark.get_deleted() is False:
			textbuffer.delete_mark(mark)
		return False
	return True

def free_line_above(textbuffer):
	"""
	Shift the text on current line to the next one.

	@param textbuffer: The text buffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Return the line freed.
	@rtype: A Integer object.
	"""
	string = None
	spaces = get_beginning_spaces(textbuffer)
	if spaces: string = "".join(spaces)
	begin_position, end_position = get_line_bounds(textbuffer)
	textbuffer.begin_user_action()
	textbuffer.insert(begin_position, "\n")
	begin_position, end_position = get_line_bounds(textbuffer)
	begin_position.backward_line()
	textbuffer.place_cursor(begin_position)
	if string: textbuffer.insert(begin_position, string)
	textbuffer.end_user_action()
	from SCRIBES.cursor import get_cursor_line
	return get_cursor_line(textbuffer)

def free_line_below(textbuffer):
	"""
	Free the line below the current one.

	@param textbuffer: The text buffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Return the line freed.
	@rtype: A Integer object.
	"""
	string = None
	spaces = get_beginning_spaces(textbuffer)
	if spaces: string = "".join(spaces)
	begin_position, end_position = get_line_bounds(textbuffer)
	textbuffer.begin_user_action()
	if begin_position.ends_line():
		textbuffer.insert(begin_position, "\n")
	else:
		textbuffer.place_cursor(end_position)
		textbuffer.insert(end_position, "\n")
	from SCRIBES.cursor import get_cursor_line, get_cursor_iterator
	iterator = get_cursor_iterator(textbuffer)
	if string: textbuffer.insert(iterator, string)
	textbuffer.end_user_action()
	return get_cursor_line(textbuffer)

def get_beginning_spaces(textbuffer):
	"""
	Get the spaces at the beginning of the current line.

	Spaces constitute either space or tab characters.

	@param textbuffer: The text buffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Return a list of spaces at the beginning of a line.
	@rtype: A List object.
	"""
	begin_position, end_position = get_line_bounds(textbuffer)
	if begin_position.ends_line(): return None
	spaces = []
	transition_position = begin_position.copy()
	while transition_position.get_char() in [" ", "\t"]:
		spaces.append(transition_position.get_char())
		transition_position.forward_char()
	return spaces

def delete_cursor_to_line_end(textbuffer):
	begin_position, end_position = get_line_bounds(textbuffer)
	if begin_position.ends_line(): return False
	from SCRIBES.cursor import get_cursor_iterator
	cursor_position = get_cursor_iterator(textbuffer)
	if cursor_position.ends_line(): return False
	textbuffer.begin_user_action()
	textbuffer.delete(cursor_position, end_position)
	textbuffer.end_user_action()
	return True

def delete_cursor_to_line_begin(textbuffer):
	begin_position, end_position = get_line_bounds(textbuffer)
	if begin_position.ends_line(): return False
	from SCRIBES.cursor import get_cursor_iterator
	cursor_position = get_cursor_iterator(textbuffer)
	if cursor_position.equal(begin_position): return False
	textbuffer.begin_user_action()
	textbuffer.delete(begin_position, cursor_position)
	textbuffer.end_user_action()
	return True

try:
	from psyco import bind
	bind(delete_cursor_to_line_begin)
	bind(delete_cursor_to_line_end)
	bind(select_line)
	bind(delete_line)
	bind(duplicate_line)
	bind(free_line_below)
	bind(free_line_above)
	bind(join_line)
	bind(get_text_on_line)
	bind(get_beginning_spaces)
except ImportError:
	pass
	