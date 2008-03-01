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
This module documents functions to store and get a list of encodings to
display in the open/save dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_database(flag="c"):
	"""
	Open encoding database.

	@return: A database object representing the encoding database.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os.path import exists, join
	preference_folder = join(metadata_folder, "Preferences")
	if not exists(preference_folder):
		from os import makedirs
		makedirs(preference_folder)
	database_file = join(preference_folder, "EncodingList.gdb")
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def get_value():
	"""
	Get list of encodings to display in open/save dialog.

	@return: A list of encodings
	@rtype: A List object.
	"""
	try:
		value = ["iso-8859-1", "iso-8859-15"]
		database = open_database("r")
		value = database["encodings"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(value):
	"""
	Set list of encodings to display in open/save dialog.

	@param value: List of encodings.
	@type value: A List object.
	"""
	database = open_database("w")
	database["encodings"] = value
	database.close()
	return
