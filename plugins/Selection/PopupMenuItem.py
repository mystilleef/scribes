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
This module documents the spaces menu item object for the text editor's popup
menu.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class SelectionPopupMenuItem(ImageMenuItem):
	"""
	This class creates the spaces popup menu item for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the popup menu item.

		@param self: Reference to the SelectionPopupMenuItem instance.
		@type self: A SelectionPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		from i18n import msg0010
		ImageMenuItem.__init__(self, msg0010)
		self.__init_attributes(editor)
		self.__creates_widgets()
		self.__set_properties()
		self.__signal_id_1 = self.select_word_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.select_line_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_3 = self.select_sentence_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_5 = self.select_word_menuitem.connect("map-event", self.__popup_word_map_event_cb)
		self.__signal_id_6 = self.select_line_menuitem.connect("map-event", self.__popup_line_map_event_cb)
		self.__signal_id_7 = self.select_sentence_menuitem.connect("map-event", self.__popup_sentence_map_event_cb)
		self.__signal_id_9 = self.scribesview.connect("focus-in-event", self.__focus_in_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the popup menu item's attributes.

		@param self: Reference to the SelectionPopupMenuItem instance.
		@type self: A SelectionPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		self.scribesview = editor.textview
		self.editor = editor
		self.menu = None
		self.image = None
		self.select_word_menuitem = None
		self.select_line_menuitem = None
		self.select_sentence_menuitem = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		self.__signal_id_7 = None
		self.__signal_id_9 = None
		return

	def __creates_widgets(self):
		"""
		Create the popup menu item's interface.

		@param self: Reference to the SelectionPopupMenuItem instance.
		@type self: A SelectionPopupMenuItem object.
		"""
		from gtk import Image, STOCK_BOLD, Menu
		self.image = Image()
		self.image.set_property("stock", STOCK_BOLD)
		self.menu = Menu()
		from i18n import msg0011, msg0012, msg0013
		from i18n import msg0014
		self.select_word_menuitem = self.editor.create_menuitem(msg0011)
		self.select_line_menuitem = self.editor.create_menuitem(msg0012)
		self.select_sentence_menuitem = self.editor.create_menuitem(msg0013)
		return

	def __set_properties(self):
		"""
		Set the menu item's properties.

		@param self: Reference to the SelectionPopupMenuItem instance.
		@type self: A SelectionPopupMenuItem object.
		"""
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.select_line_menuitem)
		self.menu.append(self.select_word_menuitem)
		self.menu.append(self.select_sentence_menuitem)
		if self.editor.is_readonly: self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SelectionPopupMenuItem instance.
		@type self: A SelectionPopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if menuitem == self.select_word_menuitem:
			self.editor.trigger("select_word")
		elif menuitem == self.select_line_menuitem:
			self.editor.trigger("select_line")
		elif menuitem == self.select_sentence_menuitem:
			self.editor.trigger("select_sentence")
		return True

	def __popup_word_map_event_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.
		"""
		menuitem.set_property("sensitive", False)
		from word import inside_word, starts_word, ends_word
		cursor_position = self.editor.get_cursor_iterator()
		if inside_word(cursor_position) or starts_word(cursor_position) or ends_word(cursor_position):
			menuitem.set_property("sensitive", True)
		return True

	def __popup_line_map_event_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.
		"""
		menuitem.set_property("sensitive", False)
		from lines import get_line_bounds
		begin_position, end_position = get_line_bounds(self.editor.textbuffer)
		if not begin_position.get_char() in ["\n", "\x00"]:
			menuitem.set_property("sensitive", True)
		return True

	def __popup_sentence_map_event_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.
		"""
		menuitem.set_property("sensitive", False)
		cursor_position = self.editor.get_cursor_iterator()
		if cursor_position.starts_sentence() or cursor_position.ends_sentence() or cursor_position.inside_sentence():
			menuitem.set_property("sensitive", True)
		return True

	def __focus_in_event_cb(self, event, textview):
		"""
		Handles callback when the "focus-in-event" signal is emitted.

		@param self: Reference to the SelectionPopupMenuItem instance.
		@type self: A SelectionPopupMenuItem object.

		@param event: An event that occurs when the editor's popup menu is displayed.
		@type event: A gtk.Event object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.editor.disconnect_signal(self.__signal_id_1, self.select_word_menuitem)
		self.editor.disconnect_signal(self.__signal_id_2, self.select_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_3, self.select_sentence_menuitem)
		self.editor.disconnect_signal(self.__signal_id_4, self.select_paragraph_menuitem)
		self.editor.disconnect_signal(self.__signal_id_5, self.select_word_menuitem)
		self.editor.disconnect_signal(self.__signal_id_6, self.select_line_menuitem)
		self.editor.disconnect_signal(self.__signal_id_7, self.select_sentence_menuitem)
		self.editor.disconnect_signal(self.__signal_id_9, self.scribesview)
		if self.select_word_menuitem: self.select_word_menuitem.destroy()
		if self.select_sentence_menuitem: self.select_sentence_menuitem.destroy()
		if self.select_line_menuitem: self.select_line_menuitem.destroy()
		if self.image: self.image.destroy()
		if self.menu: self.menu.destroy()
		del self
		self = None
		return False
