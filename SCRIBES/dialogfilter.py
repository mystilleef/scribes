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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes functions that create filter objects for the text editor's
open/save dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def create_filter(name="", mime="", pattern=""):
	"""
	Create a filter for the text editor's fileselector dialog.
	The filter is used to filter text files based on file type and source code.

	@param name: A human readable name for the text editor's fileselector
				filter.
	@type name: A string.

	@param mime: The mime type to filter.
	@type mime: A string.

	@param pattern: A regular expression pattern.
	@type pattern: A string.

	@return: A filter.
	@rtype: A gtk.FileFilter object.
	"""
	from gtk import FileFilter
	filefilter = FileFilter()
	filefilter.set_name(name)
	filefilter.add_mime_type(mime)
	if pattern: filefilter.add_pattern(pattern)
	return filefilter


def create_filter_list():
	"""
	Filter for the open and save dialog.

	@return: A list of filters.
	@rtype: A List object.
	"""
	from internationalization import msg0029, msg0028, msg0027, msg0343, msg0344
	from internationalization import msg0345, msg0346, msg0347, msg0348, msg0349
	from internationalization import msg0350, msg0351, msg0352, msg0353
	filter_list = [
		create_filter(msg0029, "text/plain"),
		create_filter(msg0028, "text/x-python"),
		create_filter(msg0343, "text/x-ruby"),
		create_filter(msg0344, "text/x-perl"),
		create_filter(msg0345, "text/csrc"),
		create_filter(msg0346, "text/c++src"),
		create_filter(msg0347, "text/csharp"),
		create_filter(msg0348, "text/x-java"),
		create_filter(msg0349, "text/x-php"),
		create_filter(msg0350, "text/html"),
		create_filter(msg0351, "text/xml"),
		create_filter(msg0352, "text/x-haskell"),
		create_filter(msg0353, "text/x-scheme"),
		create_filter(msg0027, "", "*"),
	]
	return filter_list
