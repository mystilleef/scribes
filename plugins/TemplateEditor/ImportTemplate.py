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
This module documents functions that import templates from an XML
template file to the text editor's template database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def import_template_from_file(filename):
	"""
	Import templates from an XML template file.

	@param filename: The path to the file to import templates from.
	@type filename: A String object.

	@return: True if importation succeeded.
	@rtype: A Boolean object.
	"""
	from ReadXMLTemplate import get_template_from_file
	templates = get_template_from_file(filename)
	for template_info in templates:
		add_template_to_database(template_info)
	return templates

def import_template_from_string(string):
	"""
	Import templates from an XML template string.

	@param string: A string containing an XML template.
	@type string: A String object.

	@return: True if importation succeeded.
	@rtype: A Boolean object.
	"""
	from ReadXMLTemplate import get_template_from_string
	templates = get_template_from_string(string)
	for template_info in templates:
		add_template_to_database(template_info)
	return templates

def add_template_to_database(template_info):
	"""
	Add a template to the template database.

	@param template_info: Information about a template.
	@type template_info: A Tuple object.
	"""
	template_key = template_info[0].encode("utf-8")
	template_description = template_info[1].encode("utf-8")
	template = template_info[2].encode("utf-8")
	from Metadata import open_template_database, close_template_database
	database = open_template_database("w")
	for key in database.keys():
		if template_key.startswith(key):
			if key != template_key[:len(key)]:
				continue
			count = calculate_count(database, template_key)
			if count:
				template_key = template_key + "-" + str(count)
			break
	database[template_key] = (template_description, template)
	close_template_database(database)
	return

def calculate_count(database, template_key):
	"""
	Calculate a count to append to duplicate templates.

	@param database: An object representing the templates database.
	@type database: A Shelve object.

	@param template_key: A key for a template in the database.
	@type template_key: A String object.

	@return: The count to append to a template key.
	@rtype: An Integer object.
	"""
	count = 0
	temporary_list = []
	for key in database.keys():
		if key.startswith(template_key):
			temporary_list.append(key)
	if temporary_list:
		while True:
			count += 1
			new_key = template_key
			new_key = new_key + "-" + str(count)
			if not new_key in temporary_list:
				break
	return count
