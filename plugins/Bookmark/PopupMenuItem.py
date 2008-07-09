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

from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):
	"""
	This class creates the bookmarks popup menu for the text editor.
	"""

	def __init__(self, editor):
		from i18n import msg5
		ImageMenuItem.__init__(self, msg5)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__menuitem1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__menuitem2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__menuitem3.connect("activate", self.__activate_cb)
		self.__sigid4 = self.__menuitem1.connect("map-event", self.__map_cb)
		self.__sigid5 = self.__menuitem2.connect("map-event", self.__map_cb)
		self.__sigid6 = self.__menuitem3.connect("map-event", self.__map_cb)
		self.__sigid7 = editor.textview.connect("focus-in-event", self.__destroy_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from gtk import Menu
		self.__menu = Menu()
		from os.path import join
		current_folder = self.__editor.get_current_folder(globals())
		image = join(current_folder, "bookmarks.png")
		self.__image = self.__editor.create_image(image)
		from i18n import msg6, msg7, msg8
		self.__menuitem1 = self.__editor.create_menuitem(msg6)
		self.__menuitem2 = self.__editor.create_menuitem(msg7)
		self.__menuitem3 = self.__editor.create_menuitem(msg8)
		return

	def __set_properties(self):
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__menuitem1)
		self.__menu.append(self.__menuitem2)
		self.__menu.append(self.__menuitem3)
		return

	def __activate_cb(self, menuitem):
		if menuitem == self.__menuitem1:
			self.__editor.trigger("toggle-bookmark")
		elif menuitem == self.__menuitem2:
			self.__editor.trigger("remove-all-bookmarks")
		else:
			self.__editor.trigger("show-bookmark-browser")
		return False

	def __map_cb(self, menuitem, event):
		self.__sensitize_menuitem(menuitem)
		return False

	def __sensitize_menuitem(self, menuitem):
		from Metadata import get_value
		if self.__editor.uri in (None, ""): return
		lines = get_value(self.__editor.uri)
		if menuitem in (self.__menuitem2, self.__menuitem3):
			value = True if lines else False
			menuitem.set_property("sensitive", value)
		else:
			menuitem.set_property("sensitive", True)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid2, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid3, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid4, self.__menuitem1)
		self.__editor.disconnect_signal(self.__sigid5, self.__menuitem2)
		self.__editor.disconnect_signal(self.__sigid6, self.__menuitem3)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor.textview)
		self.__menuitem1.destroy()
		self.__menuitem2.destroy()
		self.__menuitem3.destroy()
		self.__menu.destroy()
		self.__image.destroy()
		self.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
