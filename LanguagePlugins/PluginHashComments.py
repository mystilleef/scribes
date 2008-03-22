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

name = "Hash (un)comment plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["Python", "Ruby", "Perl", "sh"]
version = 0.1
autoload = True
class_name = "CommentPlugin"
short_description = "(Un)comment lines in source code"
long_description = """This plugin allows users to (un)comment lines in
hash source code by pressing (alt - c)"""

class CommentPlugin(object):
	"""
	Load and initialize comment plugin for several source code.
	"""

	def __init__(self, editor):
		"""
		Initialize the plug-in object.

		@param self: Reference to the CommentPlugin instance.
		@type self: A CommentPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None

	def load(self):
		"""
		Initialize the hash comment plugin.

		@param self: Reference to the CommentPlugin instance.
		@type self: An CommentPlugin object.
		"""
		from HashComments.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		"""
		Destroy comment plugin.

		@param self: Reference to the CommentPlugin instance.
		@type self: An CommentPlugin object.
		"""
		self.__trigger.destroy()
		return
