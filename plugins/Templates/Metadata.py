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

from SCRIBES.Utils import open_database
basepath = "templates.gdb"

def add_template_to_database(key, value):
	database = open_database(basepath, "w")
	database[str(key)] = value
	database.close()
	return

def remove_template_from_database(key):
	database = open_database(basepath, "w")
	del database[str(key)]
	database.close()
	return

def get_template_data(language):
	try:
		database = open_database(basepath, "r")
		data = []
		for key, value in database.iteritems():
			if key.startswith(language) is False: continue
	finally:
		database.close()
	return None
