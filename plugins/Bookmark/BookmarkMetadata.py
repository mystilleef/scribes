# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribe is free software; you can redistribute it and/or modify
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
This module exposes a set of functions used to store and retrieve information
about the state, size and position of text editor windows to and from a
database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_bookmark_database(flag="c"):
	"""
	Open the position database.

	@return: A database object representing the bookmark database.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os import path
	if not path.exists(metadata_folder):
		from os import makedirs
		makedirs(metadata_folder)
	database_file = metadata_folder + "bookmark.gdb"
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def close_bookmark_database(database):
	"""
	Close the position database.

	@param database: The bookmark database object.
	@type database: A database Shelve object.
	"""
	database.close()
	return

def get_bookmarks_from_database(uri):
	"""
	Get the window postion of the text editor associated with a URI.

	@param uri: A universal resource identifier representing, or pointing to, a
		file.
	@type uri: A String object.
	"""
	bookmarks = None
	database = open_bookmark_database("r")
	try:
		bookmarks = database[uri]
		close_bookmark_database(database)
	except:
		bookmarks = None
		close_bookmark_database(database)
	return bookmarks

def update_bookmarks_in_database(uri, data):
	"""
	Store the window position of the text editor.

	data is a list of bookmarked lines in the text editor's buffer.

	@param uri: A universal resource identifier representing, or pointing to, a
		file.
	@type uri: A String object.

	@param data: Bookmarked lines.
	@type data: A List object.
	"""
	database = open_bookmark_database("w")
	database[uri] = data
	close_bookmark_database(database)
	return
