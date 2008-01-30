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
All cursor and caret operations are defined in this module. The module should be
designed to be as generic as possible.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def get_cursor_iterator(textbuffer):
	"""
	Get the cursor's iterator in the text buffer.

	@param textbuffer: A text buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@return: The position of the cursor in the text buffer.
	@rtype: A gtk.TextIter object.
	"""
	cursor_mark = textbuffer.get_insert()
	cursor_iterator = textbuffer.get_iter_at_mark(cursor_mark)
	return cursor_iterator

def get_cursor_line(textbuffer):
	"""
	Return the line the cursor is on.

	@param textbuffer: A text buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@return: The line the cursor is on.
	@rtype: An Integer object.
	"""
	cursor_iterator = get_cursor_iterator(textbuffer)
	cursor_line = cursor_iterator.get_line()
	return cursor_line

def get_cursor_index(textbuffer):
	"""
	Return the index of the cursor on the cursor line.

	@param textbuffer: A text buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@return: The index of the cursor on the cursor line.
	@rtype: An Integer object.
	"""
	cursor_iterator = get_cursor_iterator(textbuffer)
	cursor_index = cursor_iterator.get_line_index()
	return cursor_index

def get_cursor_position(textview):
	"""
	Return the line and column the cursor is on.

	@param textbuffer: A text buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@return: A tuple containing line and column the cursor is on.
	@rtype: A Tuple object.
	"""
	textbuffer = textview.get_buffer()
	cursor_line = get_cursor_line(textbuffer)
	start_iterator = textbuffer.get_iter_at_line(cursor_line)
	cursor_iterator = get_cursor_iterator(textbuffer)
	line_offset = cursor_iterator.get_line_offset()
	line_text = textbuffer.get_slice(start_iterator, cursor_iterator, False)
	tabs_width = textview.get_tabs_width()
	from operator import eq, contains
	if contains(line_text, "\t"):
		for characters in line_text:
			if eq(characters, "\t"): line_offset += (tabs_width - 1)
	cursor_column = line_offset
	return cursor_line, cursor_column

def update_cursor_position(statusbar, textview):
	line, column = get_cursor_position(textview)
	from internationalization import msg0329
	string = msg0329 % ((line + 1), (column + 1))
	statusbar.pop(statusbar.context_id)
	statusbar.context_id = statusbar.get_context_id(string)
	statusbar.push(statusbar.context_id, string)
	return False

def set_textview_cursor(textview, cursor_type=None):
	"""
	Change the textview cursor to the one specified by the cursor_type
	parameter. If no cursor_type is provided, hide the textview cursor.

	@param textview: A textview object for a text buffer.
	@type textview: A gtk.TextView object.

	@param cursor_type: A bitmap image used for the mouse pointer.
	@type cursor_type: A gtk.gdk Cursor Constant.
	"""
	try:
		from gtk import TEXT_WINDOW_TEXT
		window = textview.get_window(TEXT_WINDOW_TEXT)
		from gtk.gdk import Cursor
		if cursor_type:
			window.set_cursor(Cursor(cursor_type))
		else:
			# Make the textview cursor invisible.
			from gtk.gdk import Pixmap, Color
			pixmap = Pixmap(None, 1, 1, 1)
			color = Color()
			window.set_cursor(Cursor(pixmap, pixmap, color, color, 0, 0))
	except:
		pass
	return

def show_textview_cursor(textview):
	"""
	Show the default "XTERM" textview cursor.

	@param textview: A textview object for a text buffer.
	@type textview: A gtk.TextView object.

	"""
	from gtk.gdk import XTERM
	set_textview_cursor(textview, XTERM)
	return

def hide_textview_cursor(textview):
	"""
	Hide the textview cursor.

	@param textview: A textview object for a text buffer.
	@type textview: A gtk.TextView object.

	"""
	set_textview_cursor(textview)
	return

def show_busy_textview_cursor(textview):
	"""
	Show the "WATCH" textview cursor.

	@param textview: A textview object for a text buffer.
	@type textview: A gtk.TextView object.

	"""
	from gtk.gdk import WATCH
	set_textview_cursor(textview, WATCH)
	return

def move_view_to_cursor(textview):
	textbuffer = textview.get_buffer()
	cursor_mark = textbuffer.get_insert()
	textview.scroll_to_mark(cursor_mark, 0.05, False, 0.5, 0.5)
	return

def word_to_cursor(textbuffer):
	cursor_position = get_cursor_iterator(textbuffer)
	if cursor_position.starts_line(): return None
	line = get_cursor_line(textbuffer)
	begin_position = textbuffer.get_iter_at_line(line)
	text = textbuffer.get_text(begin_position, cursor_position)
	if text:
		if not text[-1] in (" ", "\t"):
			text = text.replace("\t", " ")
			string_list = text.split(" ")
			return string_list[-1]
	return None

def get_template_trigger(textbuffer):
	cursor_position = get_cursor_iterator(textbuffer)
	if cursor_position.starts_line(): return None
	iterator = cursor_position.copy()
	iterator.backward_char()
	do_forward_char = True
	found_alphanumeric_characters = False
	while iterator.get_char().isalnum():
		found_alphanumeric_characters = True
		if iterator.starts_line():
			do_forward_char = False
			break
		iterator.backward_char()
	if found_alphanumeric_characters is False: return None
	if do_forward_char: iterator.forward_char()
	trigger = textbuffer.get_text(iterator, cursor_position)
	return trigger

def get_word_to_cursor(textbuffer):
	cursor_position = get_cursor_iterator(textbuffer)
	from word import ends_word, get_word
	from operator import not_
	if not_(ends_word(cursor_position)): return None
	word = get_word(textbuffer, cursor_position)
	return word

def get_word_before_cursor(textbuffer):
	word = get_word_to_cursor(textbuffer)
	if word and len(word) > 2: return word
	return None

def get_cursor_window_coordinates(textview):
	"""
	Get the window coordinates of the cursor in the text editor' buffer.

	@param editor: Reference to the editor object.
	@type editor: An editor object

	@return: The position of the cursor in the text editor's buffer
	@rtype: A tuple representing the x and y coordinates of the cursor's
			position in the text editor' buffer.
	"""
	# Get the cursor's iterator.
	cursor_iterator = get_cursor_iterator(textview.get_buffer())
	# Get the cursor's buffer coordinates.
	rectangle = textview.get_iter_location(cursor_iterator)
	# Get the cursor's window coordinates.
	from gtk import TEXT_WINDOW_TEXT
	position = textview.buffer_to_window_coords(TEXT_WINDOW_TEXT, rectangle.x,
											rectangle.y)
	cursor_x = position[0]
	cursor_y = position[1]
	return cursor_x, cursor_y

def get_cursor_size(textview):
	"""
	Get the cursor's size.

	@param editor: Reference to the editor object.
	@type editor: An editor object
	"""
	# Get the cursor's iterator.
	cursor_iterator = get_cursor_iterator(textview.get_buffer())
	# Get the cursor's size via its buffer coordinates.
	rectangle = textview.get_iter_location(cursor_iterator)
	cursor_width = rectangle.width
	cursor_height = rectangle.height
	return cursor_width, cursor_height

#try:
#	from psyco import bind
#	bind(get_cursor_iterator)
#	bind(update_cursor_position)
#	bind(get_cursor_size)
#	bind(get_word_before_cursor)
#	bind(get_word_to_cursor)
#	bind(get_template_trigger)
#	bind(get_cursor_line)
#	bind(get_cursor_index)
#	bind(get_cursor_window_coordinates)
#	bind(move_view_to_cursor)
#except ImportError:
#	pass
#except:
#	pass

