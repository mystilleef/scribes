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
bookmark operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: <mystilleef@gmail.com>
"""

name = "Bookmark Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "BookmarkPlugin"
short_description = "Bookmark operations."
long_description = """This plug-in performs operations to bookmark \
lines."""

class BookmarkPlugin(object):
	"""
	This class initializes a plug-in that performs selection operations.
	"""

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from Bookmark.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
