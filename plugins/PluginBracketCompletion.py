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

name = "Bracket Completion Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "BracketCompletionPlugin"
short_description = "Bracket completion operations."
long_description = """This plug-in performs bracket completion operations"""

class BracketCompletionPlugin(object):
	"""
	This class initializes a plug-in that performs bracket completion
	operations.
	"""

	def __init__(self, editor):
		"""
		Initialize the plug-in object.

		@param self: Reference to the BracketCompletionPlugin instance.
		@type self: A BracketCompletionPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None

	def load(self):
		"""
		Initialize the BracketCompletionPlugin instance.

		@param self: Reference to the BracketCompletionPlugin instance.
		@type self: An BracketCompletionPlugin object.
		"""
		from BracketCompletion.Manager import BracketManager
		self.__manager = BracketManager(self.__editor)
		return

	def unload(self):
		"""
		Destroy the BracketCompletionPlugin instance.

		@param self: Reference to the BracketCompletionPlugin instance.
		@type self: An BracketCompletionPlugin object.
		"""
		self.__manager.destroy()
		return
