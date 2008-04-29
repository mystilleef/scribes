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
This module documents a class that implements the behavior of the remove button for the theme configuration window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class RemoveButton(object):
	"""
	Implements the remove button for the theme configuration window.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("can-remove", self.__can_remove_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.glade.get_widget("RemoveButton")
		return

	def __can_remove_cb(self, manager, can_remove):
		self.__button.set_property("sensitive", can_remove)
		return True

	def __clicked_cb(self, *args):
		self.__manager.emit("remove-theme")
		return True

	def __destroy_cb(self, *args):
		self.__button.destroy()
		return True
