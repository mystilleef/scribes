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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module documents the spaces menu item object for the text editor's
popup menu.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class SpacesPopupMenuItem(ImageMenuItem):
	"""
	This class creates the spaces popup menu item for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the popup menu item.

		@param self: Reference to the SpacesPopupMenuItem instance.
		@type self: A SpacesPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		from i18n import msg0011
		ImageMenuItem.__init__(self, msg0011)
		self.__init_attributes(editor)
		self.__creates_widgets()
		self.__set_properties()
		self.__signal_id_1 = self.tabs_to_spaces_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.spaces_to_tabs_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.removes_spaces_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_4 = self.scribesview.connect("focus-in-event", self.__popup_focus_in_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the popup menu item's attributes.

		@param self: Reference to the SpacesPopupMenuItem instance.
		@type self: A SpacesPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		self.scribesview = editor.textview
		self.editor = editor
		self.menu = None
		self.image = None
		self.tabs_to_spaces_menuitem = None
		self.spaces_to_tabs_menuitem = None
		self.removes_spaces_menuitem = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __creates_widgets(self):
		"""
		Create the popup menu item's interface.

		@param self: Reference to the SpacesPopupMenuItem instance.
		@type self: A SpacesPopupMenuItem object.
		"""
		from gtk import Image, STOCK_CLEAR, Menu
		self.image = Image()
		self.image.set_property("stock", STOCK_CLEAR)
		self.menu = Menu()
		from i18n import msg0012, msg0013, msg0014
		self.tabs_to_spaces_menuitem = self.editor.create_menuitem(msg0012)
		self.spaces_to_tabs_menuitem = self.editor.create_menuitem(msg0013)
		self.removes_spaces_menuitem = self.editor.create_menuitem(msg0014)
		return

	def __set_properties(self):
		"""
		Set the menu item's properties.

		@param self: Reference to the SpacesPopupMenuItem instance.
		@type self: A SpacesPopupMenuItem object.
		"""
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.spaces_to_tabs_menuitem)
		self.menu.append(self.tabs_to_spaces_menuitem)
		self.menu.append(self.removes_spaces_menuitem)
		if self.editor.is_readonly: self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SpacesPopupMenuItem instance.
		@type self: A SpacesPopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if menuitem == self.tabs_to_spaces_menuitem:
			self.editor.trigger("tabs_to_spaces")
		elif menuitem == self.spaces_to_tabs_menuitem:
			self.editor.trigger("spaces_to_tabs")
		else:
			self.editor.trigger("remove_trailing_spaces")
		return True

	def __popup_focus_in_event_cb(self, event, textview):
		"""
		Handles callback when the "focus-in-event" signal is emitted.

		@param self: Reference to the SpacesPopupMenuItem instance.
		@type self: A SpacesPopupMenuItem object.

		@param event: An event that occurs when the editor's textview is focused.
		@type event: A gtk.Event object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.editor.disconnect_signal(self.__signal_id_1, self.tabs_to_spaces_menuitem)
		self.editor.disconnect_signal(self.__signal_id_2, self.spaces_to_tabs_menuitem)
		self.editor.disconnect_signal(self.__signal_id_3, self.removes_spaces_menuitem)
		self.editor.disconnect_signal(self.__signal_id_4, self.scribesview)
		if self.tabs_to_spaces_menuitem: self.tabs_to_spaces_menuitem.destroy()
		if self.spaces_to_tabs_menuitem: self.spaces_to_tabs_menuitem.destroy()
		if self.removes_spaces_menuitem: self.removes_spaces_menuitem.destroy()
		if self.image: self.image.destroy()
		if self.menu: self.menu.destroy()
		self.destroy()
		del self
		self = None
		return False
