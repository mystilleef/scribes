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
This module documents functions to store and get syntax colors property
from the database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_database(flag="c"):
	"""
	Open the background database.

	@return: A database object representing the syntax colors database.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os.path import exists, join
	syntax_folder = join(metadata_folder, "SyntaxColors")
	if not exists(syntax_folder):
		from os import makedirs
		makedirs(syntax_folder)
	database_file = join(syntax_folder, "SyntaxColors.gdb")
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def get_value(language_id):
	"""
	Get syntax color properties for a language from database.

	@param language_id: The language.
	@type language_id: A String object.

	@return: List of dictionary representing attributes and styles for language.
	@rtype: A List object.
	"""
	try:
		value = None
		database = open_database("r")
		value = database[language_id]
		database.close()
	except KeyError:
		database.close()
	except:
		database.close()
	return value

def set_value(language_id, keyword, styles):
	"""
	Set syntax color attributes in database.

	@param language_id: A programming language.
	@type language_id: A String object.

	@param list_of_dictionaries: Each dictionary represents attributes.
	@type list_of_dictionaries: A List object.
	"""
	# Format of the list of dictionaries.
	# ["function_name": (fgcolor, bgcolor, bold, italic, underline),
	#	"Numbers": (fgcolor, bgcolor, bold, italic, underline),
	#	"String": (fgcolor, bgcolor, bold, italic, underline)]
	lists = get_value(language_id)
	database = open_database("w")
	if lists:
		matched_dictionary = None
		for dictionary in lists:
			if dictionary.has_key(keyword):
				matched_dictionary = dictionary
				break
		if matched_dictionary: lists.remove(matched_dictionary)
		database[language_id] = lists.append({keyword: styles})
	else:
		database[language_id] = [{keyword:styles}]
	database.close()
	return

def remove_value(language_id):
	try:
		database = open_database("w")
		del database[language_id]
		database.close()
	except:
		database.close()
	return
