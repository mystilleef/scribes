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

name = "Automatic Word Replacement Graphic User Interface"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = False
class_name = "AutoReplaceGUIPlugin"
short_description = "GUI for automatic replacement."
long_description = """\
The plug-in implements a graphic user interface that allows users to
add, remove and updates words for automatic replacement. Via a graphic
user interface, a user can map the letter "u" to the word "you". Thus,
anytime the user types "u" followed by the "space" or "Enter" key, "u"
is expanded to "you".
"""

class AutoReplaceGUIPlugin(object):
	"""
	This class implements the protocol to initialize the
	"AutoReplaceGUI" plug-in.
	"""

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the AutoReplaceGUIPlugin instance.
		@type self: A AutoReplaceGUI object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None

	def load(self):
		"""
		Initialize the "AutoReplaceGUI" plug-in object.

		@param self: Reference to the AutoReplaceGUIPlugin instance.
		@type self: An AutoReplaceGUIPlugin object.
		"""
		from AutoReplaceGUI.Trigger import AutoReplaceGUITrigger
		self.__trigger = AutoReplaceGUITrigger(self.__editor)
		return

	def unload(self):
		"""
		Destroy the "AutoReplace" plug-in object.

		@param self: Reference to the AutoReplacePlugin instance.
		@type self: An AutoReplacePlugin object.
		"""
		self.__trigger.emit("destroy")
		return
