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
This module documents a class that implements the plug-in protocol for
the automatic word replacement plug-in.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

name = "Automatic Word Replacement"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "AutoReplacePlugin"
short_description = "Expand abbreviations in the buffer"
long_description = """\
The plug-in allows users to expand abbreviations in the text editor's
buffer. Via a graphic user interface, a user can map
the letter "u" to the word "you". Thus, anytime the user types "u"
followed by the "space" or "Enter" key, "u" is expanded to "you". This
plug-in implements the algorithm to perform such expansions. The user
interface for mapping abbreviations to text is implemented by another
plug-in, see "PluginAutoReplaceGUI.py".
"""

class AutoReplacePlugin(object):
	"""
	This class implements the protocol to initialize the "AutoReplace"
	plug-in.
	"""

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the AutoReplacePlugin instance.
		@type self: A AutoReplacePlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None

	def load(self):
		"""
		Initialize the "AutoReplace" plug-in object.

		@param self: Reference to the AutoReplacePlugin instance.
		@type self: An AutoReplacePlugin object.
		"""
		from AutoReplace.Manager import AutoReplaceManager
		self.__manager = AutoReplaceManager(self.__editor)
		return

	def unload(self):
		"""
		Destroy the "AutoReplace" plug-in object.

		@param self: Reference to the AutoReplacePlugin instance.
		@type self: An AutoReplacePlugin object.
		"""
		self.__manager.emit("destroy")
		return
