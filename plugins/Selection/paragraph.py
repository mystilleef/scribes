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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents functions that perform paragraph operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def select_paragraph(textbuffer):
	"""
	Select a paragraph, if any, on the current line.

	@param textbuffer: The text buffer in which to select a paragraph.
	@type textbuffer: A gtk.TextBuffer object.

	@return: Return True if a paragraph was selected.
	@rtype: A Boolean object.
	"""
	from SCRIBES.cursor import get_cursor_iterator
	cursor_position = get_cursor_iterator(textbuffer)
	if cursor_position.starts_sentence() or cursor_position.ends_sentence() or cursor_position.inside_sentence():
		end_position = cursor_position.copy()
		if cursor_position.backward_line():
			while not cursor_position.get_char() in ["\n", "\x00"]:
				result = cursor_position.backward_line()
				if not result:
					break
			if cursor_position.get_char() in ["\n", "\x00"]:
				cursor_position.forward_line()
		else:
			cursor_position.backward_sentence_start()
		if end_position.forward_line():
			while not end_position.get_char() in ["\n", "\x00"]:
				result = end_position.forward_line()
				if not result:
					break
			if end_position.get_char() in ["\n", "\x00"]:
				end_position.backward_line()
			end_position.forward_sentence_end()
		else:
			end_position.forward_sentence_end()
		textbuffer.select_range(cursor_position, end_position)
	else:
		return False
	return True
