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
This module contains functions that perform word operations. The functions are
designed to be generic and thus can be used accross this project or in any
PyGTK+ project.

For the purpose of this project, a word is a sequence of alphanumeric characters
that, optionally, may contain an underscore ("_") or a dash ("-") character.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def starts_word(iterator):
	"""
	Check if the iterator is at the beginning of a word.

	For the purpose of this project, a word is a sequence of alphanumeric
	characters that, optionally, may contain an underscore ("_") or a dash ("-")
	character.

	@param iterator: A single position in a text buffer.
	@type iterator: A gtk.TextIter object.

	@return: True if the iterator is at the beginning of a word, false otherwise.
	@rtype: A Boolean object.
	"""
	# If the iterator is at the end of a word or line then it does not start a
	# word.
	if iterator.ends_line() or iterator.ends_word(): return False
	character = iterator.get_char()
	# If the the word in front of the iterator is not alphanumeric or is not
	# an underscore or a dash, then it does not start a word.
	if character.isalnum() is False:
		if character in ("-", "_"):
			pass
		else:
			return False
	# At this point there is a valid alphanumeric character in front of the
	# iterator. So if the iterator begins a line, then it is at the start of a
	# word.
	if iterator.starts_line(): return True
	# Move the iterator back one character to determine if there is a non-
	# alphanumeric character before the real iterator position.
	iterator.backward_char()
	character = iterator.get_char()
	iterator.forward_char()
	# If there is an alphanumeric character, or an underscore, or a bash character
	# before the iterator, then the it does not start a word. Otherwise, it
	# does.
	if character.isalnum() or character in ("-", "_"): return False
	return True

def ends_word(iterator):
	"""
	Check if the iterator is at the end of a word in a text buffer.

	For the purpose of this project, a word is a sequence of alphanumeric
	characters that, optionally, may contain an underscore ("_") or a dash ("-")
	character.

	@param iterator: A single position in the text buffer.
	@type iterator: A gtk.TextIter object.

	@return: True if the iterator is at the end of a word, False otherwise.
	@rtype: A Boolean object.
	"""
	if iterator.starts_line(): return False
	character = iterator.get_char()
	if character.isalnum() or character in ("-", "_"):
		# There is a character in front of the iterator that is alphanumeric.
		return False
	iterator.backward_char()
	character = iterator.get_char()
	iterator.forward_char()
	if character.isalnum() or character in ("-", "_"):
		# There is a no alphanumeric character in front of the iterator, but
		# there is one before it. Iterator is likely at the end of a word.
		return True
	# If all else fails, return False.
	return False

def inside_word(iterator):
	"""
	Check if the iterator is inside a word.

	For the purpose of this project, a word is a sequence of alphanumeric
	characters that, optionally, may contain an underscore ("_") or a dash ("-")
	character.

	@param iterator: A single position in a text buffer.
	@type iterator: A gtk.TextIter object.

	@return: True if the iterator is inside a word, false otherwise.
	@rtype: A Boolean object.
	"""
	if starts_word(iterator) or ends_word(iterator): return False
	if iterator.starts_line() or iterator.ends_line(): return False
	character = iterator.get_char()
	if character.isalnum() is False:
		if character in ("-", "_"):
			pass
		else:
			return False
	iterator.backward_char()
	character = iterator.get_char()
	iterator.forward_char()
	if character.isalnum() is False:
		if character in ("-", "_"):
			pass
		else:
			return False
	return True

def get_word_boundary(iterator):
	"""
	Retrieve the beginning and ending position of word.

	This function determines if an iterator is at the beginning of, end of, or
	within a word. If it is, the boundaries of the word are returned, otherwise,
	nothing is returned.

	@param iterator: A single position in a text buffer.
	@type iterator: A gtk.TextIter object.

	@return: The position of a word in a text buffer or None.
	@rtype: A Tuple object containing a pair of gtk.TextIter objects or or None.
	"""
	value = None
	if starts_word(iterator):
		navigational_iterator = iterator.copy()
		while ends_word(navigational_iterator) is False:
			navigational_iterator.forward_char()
		value = iterator, navigational_iterator
	elif inside_word(iterator):
		begin_iterator = iterator.copy()
		end_iterator = iterator.copy()
		while starts_word(begin_iterator) is False:
			begin_iterator.backward_char()
		while ends_word(end_iterator) is False:
			end_iterator.forward_char()
		value = begin_iterator, end_iterator
	elif ends_word(iterator):
		navigational_iterator = iterator.copy()
		while starts_word(navigational_iterator) is False:
			navigational_iterator.backward_char()
		value = navigational_iterator, iterator
	return value

def get_word(textbuffer, iterator):
	"""
	Given a gtk.TextIter, get a word in a text buffer.

	@param textbuffer: A text buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@param iterator: A single position in a text buffer.
	@type iterator: A gtk.TextIter object.

	@return: A word around the position specified by a gtk.TextIter, or None if
		no word was found around the gtk.TextIter.
	@rtype: A String object.

	"""
	result = get_word_boundary(iterator)
	if result: result = textbuffer.get_text(result[0], result[1])
	return result

def select_word(textbuffer, iterator):
	"""
	Given a gtk.TextIter, select a word in a text buffer.

	@param textbuffer: A text buffer.
	@type textbuffer: A gtk.TextBuffer object.

	@param iterator: A single position in a text buffer.
	@type iterator: A gtk.TextIter object.

	@return: Return the position of the selected word, or none if no words were
		found for selection.
	@rtype: A Tuple object or None

	"""
	result = None
	result = get_word_boundary(iterator)
	if result:
		textbuffer.select_range(result[0], result[1])
	return result

try:
	from psyco import bind
	bind(ends_word)
	bind(get_word)
	bind(get_word_boundary)
	bind(select_word)
	bind(starts_word)
	bind(inside_word)
except ImportError:
	pass
except:
	pass
