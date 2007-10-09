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
This module documents the lines menu item object for the text editor's popup
menu.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class LinesPopupMenuItem(ImageMenuItem):
	"""
	This class creates the spaces popup menu item for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the popup menu item.

		@param self: Reference to the LinesPopupMenuItem instance.
		@type self: A LinesPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		from i18n import msg0010
		ImageMenuItem.__init__(self, msg0010)
		self.__init_attributes(editor)
		self.__creates_widgets()
		self.__set_properties()
		self.__signal_id_1 = self.delete_line_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.join_line_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.free_line_above_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_4 = self.free_line_below_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_5 = self.delete_cursor_to_end_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_6 = self.delete_cursor_to_begin_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_7 = self.scribesview.connect("focus-in-event", self.__popup_focus_in_event_cb)
		self.__signal_id_8 = self.__duplicate_line_menuitem.connect("activate", self.__popup_activate_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the popup menu item's attributes.

		@param self: Reference to the LinesPopupMenuItem instance.
		@type self: A LinesPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		self.scribesview = editor.textview
		self.editor = editor
		self.menu = None
		self.image = None
		self.delete_line_menuitem = None
		self.join_line_menuitem = None
		self.free_line_below_menuitem = None
		self.free_line_above_menuitem = None
		self.delete_cursor_to_begin_menuitem = None
		self.delete_cursor_to_end_menuitem = None
		self.__duplicate_line_menuitem = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		self.__signal_id_7 = None
		return

	def __creates_widgets(self):
		"""
		Create the popup menu item's interface.

		@param self: Reference to the LinesPopupMenuItem instance.
		@type self: A LinesPopupMenuItem object.
		"""
		from gtk import Image, STOCK_JUSTIFY_CENTER, Menu
		self.image = Image()
		self.image.set_property("stock", STOCK_JUSTIFY_CENTER)
		self.menu = Menu()
		from i18n import msg0011, msg0012, msg0013
		from i18n import msg0014, msg0015, msg0016, msg0018
		self.delete_line_menuitem = self.editor.create_menuitem(msg0011)
		self.join_line_menuitem = self.editor.create_menuitem(msg0012)
		self.free_line_below_menuitem = self.editor.create_menuitem(msg0014)
		self.free_line_above_menuitem = self.editor.create_menuitem(msg0013)
		self.delete_cursor_to_end_menuitem = self.editor.create_menuitem(msg0015)
		self.delete_cursor_to_begin_menuitem = self.editor.create_menuitem(msg0016)
		self.__duplicate_line_menuitem = self.editor.create_menuitem(msg0018)
		return

	def __set_properties(self):
		"""
		Set the menu item's properties.

		@param self: Reference to the LinesPopupMenuItem instance.
		@type self: A LinesPopupMenuItem object.
		"""
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.join_line_menuitem)
		self.menu.append(self.__duplicate_line_menuitem)
		self.menu.append(self.delete_line_menuitem)
		self.menu.append(self.free_line_below_menuitem)
		self.menu.append(self.free_line_above_menuitem)
		self.menu.append(self.delete_cursor_to_end_menuitem)
		self.menu.append(self.delete_cursor_to_begin_menuitem)
		if self.editor.is_readonly: self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesPopupMenuItem instance.
		@type self: A LinesPopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if menuitem == self.delete_line_menuitem:
			self.editor.trigger("delete_line")
		elif menuitem == self.join_line_menuitem:
			self.editor.trigger("join_line")
		elif menuitem == self.free_line_below_menuitem:
			self.editor.trigger("free_line_below")
		elif menuitem == self.free_line_above_menuitem:
			self.editor.trigger("free_line_above")
		elif menuitem == self.delete_cursor_to_begin_menuitem:
			self.editor.trigger("delete_cursor_to_begin")
		elif menuitem == self.delete_cursor_to_end_menuitem:
			self.editor.trigger("delete_cursor_to_end")
		elif menuitem == self.__duplicate_line_menuitem:
			self.editor.trigger("duplicate_line")
		return True

	def __popup_focus_in_event_cb(self, event, textview):
		"""
		Handles callback when the "focus-in-event" signal is emitted.

		@param self: Reference to the LinesPopupMenuItem instance.
		@type self: A LinesPopupMenuItem object.

		@param event: An event that occurs when the popup menu is shown.
		@type event: A gtk.Event object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.editor.disconnect_signal(self.__signal_id_8, self.__duplicate_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_1, self.delete_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_2, self.join_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_3, self.free_line_above_menuitem)
		self.editor.disconnect_signal(self.__signal_id_4, self.free_line_below_menuitem)
		self.editor.disconnect_signal(self.__signal_id_5, self.delete_cursor_to_end_menuitem)
		self.editor.disconnect_signal(self.__signal_id_6, self.delete_cursor_to_begin_menuitem)
		self.editor.disconnect_signal(self.__signal_id_7, self.scribesview)
		if self.delete_line_menuitem: self.delete_line_menuitem.destroy()
		if self.join_line_menuitem: self.join_line_menuitem.destroy()
		if self.free_line_above_menuitem: self.free_line_above_menuitem.destroy()
		if self.free_line_below_menuitem: self.free_line_below_menuitem.destroy()
		if self.delete_cursor_to_begin_menuitem: self.delete_cursor_to_begin_menuitem.destroy()
		if self.delete_cursor_to_end_menuitem: self.delete_cursor_to_end_menuitem.destroy()
		if self.__duplicate_line_menuitem: self.__duplicate_line_menuitem.destroy()
		if self.menu: self.menu.destroy()
		if self.image: self.image.destroy()
		del self
		self = None
		return False
