# -*- coding: utf-8 -*-
# Copyright (C) 2005 Lateef Alabi-Oki
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
This module defines a set of functions that provide basic text operations such
as searching for, replacing and highlighting/tagging text within text buffer.
The functions are designed to be generic and reusable across the project.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def search_for_text(txtbuf, text, begin, end):
	"""
	Search for text within a specified text buffer.

	This function searches for the text within the boundaries specified by begin
	and end in a specified text buffer. If matches are found the function
	returns the position of the found matches represented by pairs of
	gtk.TextMarks. Otherwise, the functions returns an empty List.

	@param txtbuf: Reference to the text buffer to search.
	@type editor: A gtk.TextBuffer object.

	@param text: The string to search for in the text editor's buffer.
	@type text: A String object.

	@param begin: The position in the buffer to begin searching for text.
	@type begin: A gtk.TextIter object.

	@param end: The position in the buffer to stop searching for text.
	@type end: A gtk.TextIter object.

	@return: The position of found matches in the buffer.
	@rtype: A List object containing pairs of gtk.TextIter or None.
	"""
	found_matches = []
	from gtk import TEXT_SEARCH_VISIBLE_ONLY
	while True:
		result = begin.forward_search(text, TEXT_SEARCH_VISIBLE_ONLY, end)
		if result:
			found_matches.append((result[0], result[1]))
			begin = result[1]
		else:
			break
	return found_matches

def replace_text(txtbuf, text, positions):
	"""
	Replace text at specified positions in a text buffer with one specified as
	a parameter.

	@param txtbuf: Reference to a text buffer where replacement should occur.
	@type txtbuf: A gtk.TextBuffer object.

	@param text: Text to insert into the text buffer.
	@type text: A String object.

	@param positions: Positions in the text buffer to replace text.
	@type positions: A List object containing pairs of gtk.TextMarks.
	"""
	for marks in positions:
		begin = txtbuf.get_iter_at_mark(marks[0])
		end = txtbuf.get_iter_at_mark(marks[1])
		txtbuf.delete(begin, end)
		begin = txtbuf.get_iter_at_mark(marks[0])
		txtbuf.insert(begin, text)
	return

def tag_text(txtbuf, positions, bgcolor=None, fgcolor=None, italic=False):
	u"""
	Tag text within the specified text buffer at defined locations.

	This function tags text within locations specified by "positions" in the
	function's parameter. While gtk.TextTag provides more tagging options, this
	function only exposes the background color, foreground color and italic
	tagging attributes.

	@param txtbuf: Reference to the text buffer instance.
	@type txtbuf: A gtk.TextBuffer object.

	@param positions: Positions of text to tag.
	@type positions: A List object containing pairs of gtk.TextIter.

	@param bgcolor: The background color of a text to tag.
	@type bgcolor: A String object representing a color.

	@param fgcolor: The foreground color of a text to tag.
	@type fgcolor: A String object representing a color.

	@param bold: Whether or not to make text bold
	@type bold: A Boolean object.

	@param italic: Whether or not to make text italic
	@type italic: A Boolean object.

	@return: Reference to the tag object used to tag text.
	@rtype: A gtk.TextTag object.
	"""
	tag = txtbuf.create_tag()
	if bgcolor:
		tag.set_property("background", bgcolor)
	if fgcolor:
		tag.set_property("foreground", fgcolor)
	if italic:
		from pango import STYLE_ITALIC
		tag.set_property("style", STYLE_ITALIC)
	for position in positions:
		txtbuf.apply_tag(tag, position[0], position[1])
	return tag

def select_text(txtbuf, begin, end):
	u"""
	Select text within specified boundaries in a text buffer.

	This function is wraps GTK+'s select_range function. The only difference is
	that this function accepts gtk.TextMarks as its arguments as opposed to
	gtk.TextIters. gtk.TextMarks are the preferred method of marking the text
	buffer.

	@param txtbuf: Reference to the text buffer instance.
	@type txtbuf: A gtk.TextBuffer object.

	@param begin: The opening boundary of a string.
	@type begin: A gtk.TextMark object.

	@param end: The closing boundary of a string.
	@type end: A gtk.TextMark object.
	"""
	start_iter = txtbuf.get_iter_at_mark(begin)
	end_iter = txtbuf.get_iter_at_mark(end)
	txtbuf.select_range(start_iter, end_iter)
	return

def decode_string_to_unicode(string, encoding):
	"""
	Decode a string of a particular encoding to unicode.

	@param string: A string to be decoded to unicode.
	@type string: A String object.

	@param encoding: The encoding of a string to be decoded.
	@type encoding: A String object.

	@return: A unicode string, or None if the string could not be decoded
		successfully.
	@rtype: A String object or None.
	"""
	try:
		unicode_string = string.decode(encoding)
	except UnicodeDecodeError:
		unicode_string = None
	except UnicodeError:
		unicode_string = None
	except:
		unicode_string = None
	return unicode_string

def encode_string(string, encoding):
	"""
	Encode a unicode string to a specified encoding.

	@param string: A unicode string to be encoded.
	@type string: A String object.

	@param encoding: The encoding a unicode string should be encoded to, or None
		if the string could not be encoded.
	@type encoding: A String object or None.
	"""
	try:
		encoded_string = string.encode(encoding)
	except UnicodeEncodeError:
		encoded_string = None
	except UnicodeError:
		encoded_string = None
	except:
		encoded_string = None
	return encoded_string
