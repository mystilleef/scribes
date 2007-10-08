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
This module documents a class that implements the popup menu item for
changing the case of selected text.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class CasePopupMenuItem(ImageMenuItem):
	"""
	This class creates the case menu item for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the menu item.

		@param self: Reference to the CasePopupMenuItem instance.
		@type self: A CasePopupMenuItem object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from i18n import msg0009
		ImageMenuItem.__init__(self, msg0009)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = self.__uppercase_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.__lowercase_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.__titlecase_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_4 = self.__swapcase_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_5 = self.__uppercase_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_6 = self.__lowercase_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_7 = self.__titlecase_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_8 = self.__swapcase_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_9 = self.__editor.textview.connect("focus-in-event", self.__popup_focus_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the menu item's data attributes.

		@param self: Reference to the CasePopupMenuItem instance.
		@type self: A CasePopupMenuItem object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from i18n import msg0010, msg0011, msg0012
		from i18n import msg0013
		from gtk import Menu, Image, STOCK_SORT_DESCENDING
		self.__image = Image()
		self.__image.set_property("stock", STOCK_SORT_DESCENDING)
		self.__editor = editor
		self.__menu = Menu()
		self.__uppercase_menuitem = editor.create_menuitem(msg0010)
		self.__lowercase_menuitem = editor.create_menuitem(msg0011)
		self.__titlecase_menuitem = editor.create_menuitem(msg0012)
		self.__swapcase_menuitem = editor.create_menuitem(msg0013)
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		self.__signal_id_7 = None
		self.__signal_id_8 = None
		self.__signal_id_9 = None
		return

	def __set_properties(self):
		"""
		Define the properties of the menu item.

		@param self: Reference to the CasePopupMenuItem instance.
		@type self: A CasePopupMenuItem object.
		"""
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__uppercase_menuitem)
		self.__menu.append(self.__lowercase_menuitem)
		self.__menu.append(self.__titlecase_menuitem)
		self.__menu.append(self.__swapcase_menuitem)
		if self.__editor.is_readonly:
			self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CasePopupMenuItem instance.
		@type self: A CasePopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if menuitem == self.__uppercase_menuitem:
			self.__editor.trigger("uppercase")
		elif menuitem == self.__lowercase_menuitem:
			self.__editor.trigger("lowercase")
		elif menuitem == self.__titlecase_menuitem:
			self.__editor.trigger("titlecase")
		elif menuitem == self.__swapcase_menuitem:
			self.__editor.trigger("swapcase")
		return True

	def __popup_map_event_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.

		@param self: Reference to the CasePopupMenuItem instance.
		@type self: A CasePopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
	#	selection = self.__editor.textbuffer.get_selection_bound()
	#	menuitem.set_property("sensitive", False)
	#	if selection is None:
	#		menuitem.set_property("sensitive", True)
		return True

	def __popup_focus_event_cb(self, textview, event):
		"""
		Handles callback when the "focus-in-event" signal is emitted.

		@param self: Reference to the CasePopupMenuItem instance.
		@type self: A CasePopupMenuItem object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param event: An event that occurs when the editor's view is focused.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__uppercase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__lowercase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__titlecase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__swapcase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__uppercase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__lowercase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__titlecase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__swapcase_menuitem)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor.textview)
		if self.__uppercase_menuitem: self.__uppercase_menuitem.destroy()
		if self.__lowercase_menuitem: self.__lowercase_menuitem.destroy()
		if self.__titlecase_menuitem: self.__titlecase_menuitem.destroy()
		if self.__swapcase_menuitem: self.__swapcase_menuitem.destroy()
		if self.__menu: self.__menu.destroy()
		if self.__image: self.__image.destroy()
		self.destroy()
		del self
		self = None
		return False
