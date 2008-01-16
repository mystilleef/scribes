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
about the encoding of a URI to and from a database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_encoding_database(flag="c"):
	"""
	Open the encoding database.

	@return: A database object representing the encoding database.
	@rtype: A database Shelve object.
	"""
	from info import metadata_folder
	from os import path
	if not path.exists(metadata_folder):
		from os import makedirs
		makedirs(metadata_folder)
	database_file = metadata_folder + "encoding.gdb"
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def close_encoding_database(database):
	"""
	Close the encoding database.

	@param database: The encoding database object.
	@type database: A database Shelve object.
	"""
	database.close()
	return


def get_encoding_from_database(uri):
	"""
	Get the encoding for a URI.

	@param uri: A universal resource identifier representing, or pointing to, a
		file.
	@type uri: A String object.
	"""
	database = open_encoding_database("r")
	try:
		encoding = database[uri]
		close_encoding_database(database)
	except:
		encoding = None
		close_encoding_database(database)
	return encoding

def update_encoding_in_database(uri, data):
	"""
	Store the encoding of the URI in the encoding database.

	data is string representing an encoding for a URI. The database format is as
	follows:

		URI : "encoding"

	@param uri: A universal resource identifier representing, or pointing to, a
		file.
	@type uri: A String object.

	@param data: Information representing the encoding of a URI
	@type data: A String object
	"""
	database = open_encoding_database("w")
	database[str(uri)] = data
	close_encoding_database(database)
	return
