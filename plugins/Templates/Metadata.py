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
templates from a database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def open_template_database(flag="r"):
	"""
	Open the template database.

	@return: A database object representing the template database.
	@rtype: A database Shelve object.
	"""
	from SCRIBES.info import metadata_folder
	from os import path
	if not path.exists(metadata_folder):
		from os import makedirs
		makedirs(metadata_folder)
	database_file = metadata_folder + "templates.gdb"
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def close_template_database(database):
	"""
	Close the template database.

	@param database: The template database object.
	@type database: A database Shelve object.
	"""
	database.close()
	return

def add_template_to_database(key, value):
	"""
	Add a template to the template database.

	@param key: The template trigger.
	@type key: A String object.

	@param value: A template for the editor.
	@type value: A String object.
	"""
	database = open_template_database("w")
	database[str(key)] = value
	close_template_database(database)
	return

def remove_template_from_database(key):
	"""
	Remove a template from the template database.

	@param key: The template trigger.
	@type key: A String object.
	"""
	database = open_template_database("w")
	del database[str(key)]
	close_template_database(database)
	return
