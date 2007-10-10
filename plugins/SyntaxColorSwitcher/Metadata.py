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
This module exposes a set of functions used to store and retrieve
syntax information from a database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_syntax_database(flag="c"):
	"""
	Open the syntax database.

	@return: A database object representing the syntax database.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os import path
	if not path.exists(metadata_folder):
		from os import makedirs
		makedirs(metadata_folder)
	database_file = metadata_folder + "syntax.gdb"
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def close_syntax_database(database):
	"""
	Close the syntax database.

	@param database: The syntax database object.
	@type database: A database Shelve object.
	"""
	database.close()
	return False

def update_database(file, language):
	"""
	Update the syntax database.

	@param key: The template trigger.
	@type key: A String object.

	@param value: A template for the editor.
	@type value: A String object.
	"""
	database = open_syntax_database("w")
	database[file] = language
	close_syntax_database(database)
	return False

def get_syntax_language(file):
	language = None
	database = open_syntax_database("r")
	from operator import contains
	if contains(database.keys(), file):
		language = database[file]
	else:
		close_syntax_database(database)
		from Exceptions import NoDataError
		raise NoDataError
	close_syntax_database(database)
	return language
