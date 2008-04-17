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
This module documents a class that implements the plug-in protocol to
show the about dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: <mystilleef@gmail.com>
"""

name = "Python Symbol Browser"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.1
autoload = True
class_name = "SymbolBrowserPlugin"
short_description = "Show symbols in python source code."
long_description = """This plugin allows users to view all symbols in
python source code and navigate to them easily. Press F5 to show the
symbol browser."""

class SymbolBrowserPlugin(object):
	"""
	Load and initialize symbol browser plugin for python source code.
	"""

	def __init__(self, editor):
		"""
		Initialize the plug-in object.

		@param self: Reference to the SymbolBrowserPlugin instance.
		@type self: A SymbolBrowserPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None

	def load(self):
		"""
		Initialize the symbol browser plugin.

		@param self: Reference to the SymbolBrowserPlugin instance.
		@type self: An SymbolBrowserPlugin object.
		"""
		from PythonSymbolBrowser.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		"""
		Destroy symbol browser plugin.

		@param self: Reference to the SymbolBrowserPlugin instance.
		@type self: An SymbolBrowserPlugin object.
		"""
		self.__trigger.destroy()
		return
