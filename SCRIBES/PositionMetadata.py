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

def open_position_database(flag="c"):
	from Globals import metadata_folder
	from os import path
	if not path.exists(metadata_folder):
		from os import makedirs
		makedirs(metadata_folder)
	database_file = metadata_folder + "position.gdb"
	from shelve import open
	from anydbm import error
	try:
		database = open(database_file, flag=flag, writeback=False)
	except error:
		database = open(database_file, flag="n", writeback=False)
	return database

def close_position_database(database):
	database.close()
	return

def get_window_position_from_database(uri):
	database = open_position_database("r")
	try:
		window_position = database[uri]
		close_position_database(database)
	except:
		window_position = None
		close_position_database(database)
	return window_position

def update_window_position_in_database(uri, data):
	database = open_position_database("w")
	database[str(uri)] = data
	close_position_database(database)
	return
