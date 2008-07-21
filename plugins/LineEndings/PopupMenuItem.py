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

from gtk import MenuItem

class PopupMenuItem(MenuItem):
	"""
	This class creates the bookmarks popup menu for the text editor.
	"""

	def __init__(self, editor):
		from i18n import msg7
		MenuItem.__init__(self, msg7)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = editor.textview.connect("focus-in-event", self.__destroy_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import Menu
		self.__menu = Menu()
		from i18n import msg4, msg5, msg6
		self.__menuitem1 = self.__editor.create_menuitem(msg4)
		self.__menuitem2 = self.__editor.create_menuitem(msg5)
		self.__menuitem3 = self.__editor.create_menuitem(msg6)
		return

	def __set_properties(self):
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("line-endings-to-unix")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("line-endings-to-mac")
		else:
			self.__editor.trigger("line-endings-to-windows")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor.textview)
		self.__menuitem1.destroy()
		self.__menuitem2.destroy()
		self.__menuitem3.destroy()
		self.__menu.destroy()
		self.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
