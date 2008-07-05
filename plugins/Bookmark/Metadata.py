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

def open_database(flag="c"):
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

def get_value(uri):
	try:
		database = open_database("r")
		bookmarks = database[uri]
	except KeyError:
		bookmarks = None
	finally:
		database.close()
	return bookmarks

def set_value(uri, data):
	try:
		if uri in (None, ""): return
		database = open_database("w")
		if data:
			database[uri] = data
		else:
			del database[uri]
	except:
		pass
	finally:
		database.close()
	return
