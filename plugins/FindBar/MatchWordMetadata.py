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
This module documents functions to store and get configuration options
to enable or disable word matching during searches.

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
	database_file = join(preference_folder, "MatchWord.gdb")
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def get_value():
	"""
	Get match word value from database.

	@return: True/False to enable/disable word matching.
	@rtype: A Boolean object.
	"""
	try:
		value = False
		database = open_database("r")
		value = database["match_word"]
	except KeyError:
		pass
	finally:
		database.close()
	return value

def set_value(match_word):
	"""
	Set match word value in database.

	@param match_case: True/False to enable/disable word matching.
	@type match_case: A Boolean object.
	"""
	try:
		database = open_database("w")
		database["match_word"] = match_word
	finally:
		database.close()
	return
