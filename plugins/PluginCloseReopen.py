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

name = "CloseReopen Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "CloseReopenPlugin"
short_description = "Close current window, reopen new one."
long_description = """Close current window, reopen new one."""

class CloseReopenPlugin(object):
	"""
	This class loads the plugin that closes the current window and opens
	a new one.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the CloseReopenPlugin loader.
		@type self: An CloseReopen object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor

	def load(self):
		"""
		Load the about plugin.

		@param self: Reference to the CloseReopenPlugin loader.
		@type self: An CloseReopenPlugin object.
		"""
		from CloseReopen.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		"""
		Unload the about plugin.

		@param self: Reference to the CloseReopenPlugin loader.
		@type self: An CloseReopenPlugin object.
		"""
		self.__trigger.destroy()
		return
