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
This module documents a class that implements the indentation popup menu item
for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class IndentPopupMenuItem(ImageMenuItem):
	"""
	This class creates the indentation popup menu item for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the popup menu item.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: A IndentPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		from i18n import msg0008
		ImageMenuItem.__init__(self, msg0008)
		self.__init_attributes(editor)
		self.__create_wigets()
		self.__set_properties()
		self.__signal_id_1 = self.indent_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.unindent_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.unindent_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_4 = self.scribesview.connect("focus-in-event", self.__popup_focus_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the popup menu item's attributes.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: A IndentPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		self.scribesview = editor.textview
		self.editor = editor
		self.menu = None
		self.image = None
		self.indent_menuitem = None
		self.unindent_menuitem = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __create_wigets(self):
		"""
		Create the popup menu item's interface.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: A IndentPopupMenuItem object.
		"""
		from gtk import Image, STOCK_JUSTIFY_CENTER, Menu
		self.image = Image()
		self.image.set_property("stock", STOCK_JUSTIFY_CENTER)
		self.menu = Menu()
		from SCRIBES.utils import create_menuitem
		from i18n import msg0009, msg0010
		from gtk import STOCK_UNINDENT, STOCK_INDENT
		self.indent_menuitem = create_menuitem(msg0009, STOCK_INDENT)
		self.unindent_menuitem = create_menuitem(msg0010, STOCK_UNINDENT)
		return

	def __set_properties(self):
		"""
		Set the menu item's properties.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: A IndentPopupMenuItem object.
		"""
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.indent_menuitem)
		self.menu.append(self.unindent_menuitem)
		if self.editor.is_readonly:
			self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: A IndentPopupMenuItem object.

		@param menuitem: A menuitem for the IndentPopupMenuItem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if menuitem == self.indent_menuitem:
			self.editor.triggermanager.trigger("indent_line")
		if menuitem == self.unindent_menuitem:
			self.editor.triggermanager.trigger("unindent_line")
		return True

	def __popup_map_event_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.

		This function determines whether or not the unindent menuitem should be
		enabled.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: A IndentPopupMenuItem object.

		@param menuitem: The the unindent menu item.
		@type menuitem: A gtk.MenuItem object.

		@param event: An event that occurs when the unindent menu item is displayed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		menuitem.set_property("sensitive", False)
		from SCRIBES.cursor import get_cursor_line
		cursor_line = get_cursor_line(self.editor.textbuffer)
		begin_position = self.editor.textbuffer.get_iter_at_line(cursor_line)
		try:
			begin_selection, end_selection = self.editor.textbuffer.get_selection_bounds()
		except ValueError:
			if begin_position.get_char() in [" ", "\t"]:
				menuitem.set_property("sensitive", True)
			else:
				menuitem.set_property("sensitive", False)
			return True
		first_selected_line = begin_selection.get_line()
		last_selected_line = end_selection.get_line()
		if first_selected_line == last_selected_line:
			if begin_position.get_char() in [" ", "\t"]:
				menuitem.set_property("sensitive", True)
			else:
				menuitem.set_property("sensitive", False)
			return True
		indentation_is_possible = False
		for line in range(first_selected_line, last_selected_line+1):
			begin_position = self.editor.textbuffer.get_iter_at_line(line)
			if begin_position.get_char() in [" ", "\t"]:
				indentation_is_possible = True
		menuitem.set_property("sensitive", indentation_is_possible)
		return True

	def __popup_focus_event_cb(self, event, textview):
		"""
		Handles callback when the "focus-in-event" event is emitted.

		This function destroys this object when the textview's
		popup menu is hidden.

		@param self: Reference to the IndentPopupMenuItem instance.
		@type self: An IndentPopupMenuItem object.

		@param event: An event emitted when the editor's textview gains focus.
		@type event: A gtk.Event object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if self.__signal_id_1 and self.indent_menuitem.handler_is_connected(self.__signal_id_1):
			self.indent_menuitem.disconnect(self.__signal_id_1)
		if self.__signal_id_2 and self.unindent_menuitem.handler_is_connected(self.__signal_id_2):
			self.unindent_menuitem.disconnect(self.__signal_id_2)
		if self.__signal_id_3 and self.unindent_menuitem.handler_is_connected(self.__signal_id_3):
			self.unindent_menuitem.disconnect(self.__signal_id_3)
		if self.__signal_id_4 and self.scribesview.handler_is_connected(self.__signal_id_4):
			self.scribesview.disconnect(self.__signal_id_4)
		if self.indent_menuitem:
			self.indent_menuitem.destroy()
		if self.unindent_menuitem:
			self.unindent_menuitem.destroy()
		if self.menu:
			self.menu.destroy()
		if self.image:
			self.image.destroy()
		self.destroy()
		del self.indent_menuitem, self.unindent_menuitem, self.menu
		del self.image, self.__signal_id_1, self.__signal_id_2
		del self.__signal_id_3, self.__signal_id_4, self.scribesview
		del self.editor, self
		self = None
		return False
