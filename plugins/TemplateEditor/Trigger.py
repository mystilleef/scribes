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
This module documents a class that creates a trigger that shows the
template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates an object that shows the text editor's template
	editor.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__show_editor_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger = self.__create_trigger()
		self.__sigid1 = None
		from MenuItem import MenuItem
		self.__menuitem = MenuItem(editor)
		return

	def __create_trigger(self):
		# Trigger to show the about dialog.
		trigger = self.__editor.create_trigger("show_template_editor", "alt+F12")
		self.__editor.add_trigger(trigger)
		return trigger

	def __show_editor_cb(self, trigger):
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__menuitem.destroy()
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		del self
		self = None
		return
