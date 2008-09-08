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

from Utils import open_database
basepath = "position.gdb"

def get_window_position_from_database(uri):
	try:
		database = open_database(basepath, "r")
		window_position = database[uri]
	except KeyError:
		window_position = None
	finally:
		database.close()
	return window_position

def update_window_position_in_database(uri, data):
	try:
		database = open_database(basepath, "w")
		database[str(uri)] = data
	finally:
		database.close()
	return
