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
This module documents functions to store and get lexical highlight
color.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_database(flag="c"):
	"""
	Open database.

	@return: A database object.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os.path import exists, join
	preference_folder = join(metadata_folder, "PluginPreferences")
	if not exists(preference_folder):
		from os import makedirs
		makedirs(preference_folder)
	database_file = join(preference_folder, "LexicalScopeHighlight.gdb")
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def get_value():
	"""
	Get color value from database.

	@return: Lexical highlight color.
	@rtype: A String object.
	"""
	try:
		value = "orange"
		database = open_database("r")
		value = database["color"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(color):
	"""
	Set color value in database.

	@param color: Lexical highligt color
	@type color: A String object.
	"""
	try:
		database = open_database("w")
		database["color"] = color
	finally:
		database.close()
	return
