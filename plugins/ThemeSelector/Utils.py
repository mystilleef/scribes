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
This module documents utility function that manipulate the GtkSourceView2
theme manager

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

def remove_theme(filename):
	from os.path import exists
	if not exists(filename): return
	from os import remove
	remove(filename)
	return

def __get_scheme_data(manager, id_, home_folder):
	scheme = manager.get_scheme(id_)
	name = scheme.get_name() + " - " + scheme.get_description()
	removable = scheme.get_filename().startswith(home_folder)
	return name, scheme, removable

def get_treeview_data(manager, home_folder):
	manager.force_rescan()
	get_scheme_data = lambda id_: __get_scheme_data(manager, id_, home_folder)
	treeview_data = map(get_scheme_data, set(manager.get_scheme_ids()))
	return treeview_data

def change_theme(scheme_id):
	from ColorThemeMetadata import set_value
	set_value(scheme_id)
	return 