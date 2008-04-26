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


def __get_gedit_sytle_path(home_folder):
	from os.path import join, exists
	base_path = ".gnome2/gedit/styles"
	gedit_path = join(home_folder, base_path)
	if exists(gedit_path): return gedit_path
	return None

def __get_scribes_style_path(home_folder):
	from os.path import join, exists
	base_path = ".gnome2/scribes/styles"
	scribes_path = join(home_folder, base_path)
	if exists(scribes_path): return scribes_path
	return None

def __update_manager_search_path(manager, home_folder):
	gedit_path = __get_gedit_sytle_path(home_folder)
	scribes_path = __get_scribes_style_path(home_folder)
	search_paths = manager.get_search_path()
	if gedit_path and not (gedit_path in search_paths): manager.prepend_search_path(gedit_path)
	if scribes_path and not (scribes_path in search_paths): manager.prepend_search_path(scribes_path)
	manager.force_rescan()
	return

def __get_scheme_data(manager, id_, home_folder):
	scheme = manager.get_scheme(id_)
	name = scheme.get_name() + " - " + scheme.get_description()
	removable = scheme.get_filename().startswith(home_folder)
	return name, scheme, removable

def get_treeview_data(manager, home_folder):
	__update_manager_search_path(manager, home_folder)
	get_scheme_data = lambda id_: __get_scheme_data(manager, id_, home_folder)
	treeview_data = map(get_scheme_data, manager.get_scheme_ids())
	return treeview_data


