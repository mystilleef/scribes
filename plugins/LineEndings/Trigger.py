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
This module documents a class that creates triggers to perform line ending
operations (i.e converting line endings to unix/mac/windows).

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.textview.connect_after("populate-popup", self.__popup_cb)
		self.__sigid2 = self.__trigger1.connect("activate", self.__to_unix_cb)
		self.__sigid3 = self.__trigger2.connect("activate", self.__to_mac_cb)
		self.__sigid4 = self.__trigger3.connect("activate", self.__to_windows_cb)

	def __init_attributes(self, editor):
		self.__manager = None
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("line-endings-to-unix", "alt - 1")
		self.__trigger2 = self.__create_trigger("line-endings-to-mac", "alt - 2")
		self.__trigger3 = self.__create_trigger("line-endings-to-windows", "alt - 3")
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3)
		self.__editor.remove_triggers(triggers)
		if self.__manager: self.__manager.destroy()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid4, self.__trigger3)
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		from PopupMenuItem import PopupMenuItem
		menu.prepend(PopupMenuItem(self.__editor))
		menu.show_all()
		return False

	def __to_unix_cb(self, *args):
		try:
			self.__manager.to_unix()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.to_unix()
		return False

	def __to_mac_cb(self, *args):
		try:
			self.__manager.to_mac()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.to_mac()
		return False

	def __to_windows_cb(self, *args):
		try:
			self.__manager.to_windows()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.to_windows()
		return False
