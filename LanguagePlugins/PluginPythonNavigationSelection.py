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
This module documents a class that loads the navigation and selection
plugins for Python source code.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: <mystilleef@gmail.com>
"""

name = "Navigation and selection plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.1
autoload = True
class_name = "NavigationSelectionPlugin"
short_description = "Navigation and selection for Python source code."
long_description = """Navigation and selection for Python source code."""

class NavigationSelectionPlugin(object):
	"""
	This class loads and unloads the navigation and selection plugin
	for Python source code.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the NavigationSelectionPlugin instance.
		@type self: A NavigationSelectionPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None

	def load(self):
		"""
		Load navigation and selection plugin.

		@param self: Reference to the NavigationSelectionPlugin instance.
		@type self: An NavigationSelectionPlugin object.
		"""
		from PythonNavigationSelection.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		"""
		Unload navigation and selection plugin.

		@param self: Reference to the NavigationSelectionPlugin instance.
		@type self: An NavigationSelectionPlugin object.
		"""
		self.__trigger.destroy()
		return
