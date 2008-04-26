# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This module documents functions to store and get the spell check
property from the database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

def open_database(flag="c"):
	"""
	Open the color theme database.

	@return: A database object representing the color theme database.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os.path import exists, join
	preference_folder = join(metadata_folder, "Preferences")
	if not exists(preference_folder):
		from os import makedirs
		makedirs(preference_folder)
	database_file = join(preference_folder, "ColorTheme.gdb")
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def get_value():
	"""
	Get spell check properties from database.

	@return: The name of a color scheme
	@rtype: A String object.
	"""
	try:
		value = "oblivion"
		database = open_database("r")
		value = database["theme"]
	except:
		database.close()
	finally:
		database.close()
	return value

def set_value(value):
	"""
	Set color theme in database.

	@param value: The name of a color theme.
	@type value: A String object.
	"""
	try:
		database = open_database("w")
		database["theme"] = value
	finally:
		database.close()
	return
