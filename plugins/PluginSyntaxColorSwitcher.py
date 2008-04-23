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
This module documents a class sets syntax colors via the popup menu.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: <mystilleef@gmail.com>
"""

name = "Syntax Color Switcher Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = False
class_name = "SyntaxColorSwitcherPlugin"
short_description = "Switch syntax colors"
long_description = """This plugin enables users to set syntax colors \
for documents for a specific language via the popup menu.
"""

class SyntaxColorSwitcherPlugin(object):
	"""
	This class initializes a plug-in that sets syntax colors.
	"""

	def __init__(self, editor):
		"""
		Initialize the plug-in object.

		@param self: Reference to the SyntaxColorSwitcherPlugin instance.
		@type self: A SyntaxColorSwitcherPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None

	def load(self):
		"""
		Initialize the SyntaxColorSwitcherPlugin instance.

		@param self: Reference to the SyntaxColorSwitcherPlugin instance.
		@type self: An SyntaxColorSwitcherPlugin object.
		"""
		from SyntaxColorSwitcher.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		"""
		Destroy the SyntaxColorSwitcherPlugin instance.

		@param self: Reference to the SyntaxColorSwitcherPlugin instance.
		@type self: An SyntaxColorSwitcherPlugin object.
		"""
		self.__manager.emit("destroy")
		return
