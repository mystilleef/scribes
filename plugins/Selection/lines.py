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
This module documents functions that selects a line in the editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright (c) 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def get_line_bounds(textbuffer):
	"""
	Get the beginning and end position of a line in a gtk.TextBuffer.

	@param textbuffer: The textbuffer to operate on.
	@type textbuffer: A gtk.TextBuffer object.

	@return: The beginning and end position of a line.
	@rtype: A Tuple object containing a pair of gtk.TextIter.
	"""
	from SCRIBES.cursor import get_cursor_line
	cursor_line = get_cursor_line(textbuffer)
	begin_position = textbuffer.get_iter_at_line(cursor_line)
	end_position = begin_position.copy()
	end_position.forward_to_line_end()
	return begin_position, end_position

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
	if begin_position.get_char() in ["\n", "\x00"]: return False
	textbuffer.select_range(begin_position, end_position)
	return True
