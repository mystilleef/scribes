# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
This module documents a class that creates a trigger to undo or redo
text operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates an object, a trigger, that undoes or redoes text
	operations.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__undo_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__redo_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("undo", "ctrl - z")
		self.__trigger2 = self.__create_trigger("redo", "ctrl - shift - z")
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __undo_cb(self, *args):
		self.__editor.undo()
		return False

	def __redo_cb(self, *args):
		self.__editor.redo()
		return

	def __destroy(self):
		self.__editor.remove_trigger(self.__trigger1)
		self.__editor.remove_trigger(self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return False
