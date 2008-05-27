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
This module contains functions that interface with the text editor's cursor
database. The cursor database contains information about the last position of
the cursor of each URI opened by the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_cursor_database(flag="c"):
	"""
	Open the cursor database.

	@return: A database object representing the cursor database.
	@rtype: A handle to the database object.
	"""
	from info import metadata_folder
	from os import path
	if not path.exists(metadata_folder):
		from os import makedirs
		makedirs(metadata_folder)
	database_file = metadata_folder + "cursor.gdb"
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def close_cursor_database(database):
	"""
	Close the cursor database.

	@param database: The handle of the cursor database object.
	@type database: A database Shelve object.
	"""
	database.close()
	return


def get_cursor_position_from_database(uri):
	"""
	Get the cursor postion associated with the URI from the cursor database.

	@param uri: A universal resource identifier representing, or pointing to, a
		file.
	@type uri: A String object.
	"""
	database = open_cursor_database("r")
	try:
		cursor_position = database[uri]
		close_cursor_database(database)
	except:
		cursor_position = None
		close_cursor_database(database)
	return cursor_position


def update_cursor_position_in_database(uri, data):
	"""
	Store the cursor position of the text editor in the cursor database.

	data is tuple object that contains the following information pertaining to
	the text editor's cursor position:

		(line, column)

	@param uri: A universal resource identifier representing, or pointing to, a
		file.
	@type uri: A String object.

	@param data: Information representing the line and column the cursor is on
		in the text editor's buffer.
		editor window.
	@type data: A Tuple object.

	"""
	database = open_cursor_database("w")
	database[str(uri)] = data
	close_cursor_database(database)
	return False

