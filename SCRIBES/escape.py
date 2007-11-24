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

u"""
This module provides function to convert strings that may contain invalid
characters to one that does not. GConf and gtksourceview are examples of APIs
that pose such problems. Characters like space, plus, opening and closing
brackets are escaped to prevent the possibilities of errors caused by invalid
characters.

"""

def generate_escape_key_dictionary():
	u"""
	Generate a dictionary containing escape keys and the characters they
	represent.

	@return: A dictionary containing escape key and character pairs.
	@rtype: A dictionary object.

	"""

	dictionary = {
		"@32@": " ",
		"@35@": "#",
		"@39@": "'",
		"@40@": "(",
		"@41@": ")",
		"@43@": "+",
		"@44@": ",",
		"@46@": ".",
		"@47@": "/",
	}

	return dictionary


def escape_string(string):
	"""
	Replace characters in a string that are difficult to parse with valid ones.

	@param string: An arbitrary string.
	@type string: A string object.

	@return: A string that has been escaped.
	@rtype: A string object.
	"""
	dictionary = generate_escape_key_dictionary()
	for escape_characters in dictionary.keys():
		escaped_string = string.replace(dictionary[escape_characters], escape_characters)
		string = escaped_string
	return escaped_string


def unescape_string(string):
	"""
	Replace escaped characters in a string with normal characters.

	@param string: An arbitrary string.
	@type string: A string object.

	@return: A string that has been escaped.
	@rtype: A string object.
	"""
	dictionary = generate_escape_key_dictionary()
	for escape_characters in dictionary.keys():
		unescaped_string = string.replace(escape_characters, dictionary[escape_characters])
		string = unescaped_string
	return unescaped_string

