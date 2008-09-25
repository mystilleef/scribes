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
This module documents a class that loads the about plugin.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

name = "Smart Space Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = False
class_name = "SmartSpacePlugin"
short_description = "Smart space plugin."
long_description = """Smart space plugin."""

class SmartSpacePlugin(object):
	"""
	This class loads the plugin that shows the about dialog.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the AboutPlugin loader.
		@type self: An AboutPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None

	def load(self):
		"""
		Load the about plugin.

		@param self: Reference to the AboutPlugin loader.
		@type self: An AboutPlugin object.
		"""
		from SmartSpace.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		"""
		Unload the about plugin.

		@param self: Reference to the AboutPlugin loader.
		@type self: An AboutPlugin object.
		"""
		self.__manager.destroy()
		return
