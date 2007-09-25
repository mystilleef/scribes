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

class BookmarkPopupMenuItem(ImageMenuItem):
	"""
	This class creates the bookmarks popup menu for the text editor.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize the popup menu.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		from i18n import msg0012
		ImageMenuItem.__init__(self, msg0012)
		self.__init_attributes(editor, manager)
		self.__create_widgets()
		self.__set_properties()
		self.__signal_id_1 = self.bookmark_line_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.remove_bookmark_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_3 = self.remove_bookmark_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_4 = self.remove_all_bookmarks_menuitem.connect("map-event", self.__popup_map_event2_cb)
		self.__signal_id_5 = self.remove_all_bookmarks_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_6 = self.next_bookmark_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_7 = self.next_bookmark_menuitem.connect("map-event", self.__popup_map_event2_cb)
		self.__signal_id_8 = self.previous_bookmark_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_9 = self.previous_bookmark_menuitem.connect("map-event", self.__popup_map_event2_cb)
		self.__signal_id_10 = self.first_bookmark_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_11 = self.first_bookmark_menuitem.connect("map-event", self.__popup_map_event2_cb)
		self.__signal_id_12 = self.last_bookmark_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_13 = self.last_bookmark_menuitem.connect("map-event", self.__popup_map_event2_cb)
		self.__signal_id_14 = self.show_browser_menuitem.connect("activate", self.__popup_activate_cb)
		self.__signal_id_15 = self.show_browser_menuitem.connect("map-event", self.__popup_map_event_cb)
		self.__signal_id_16 = self.scribesview.connect("focus-in-event", self.__popup_destroy_cb)

	def __init_attributes(self, editor, manager):
		"""
		Initialize the popup's attributes.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.

		@param scribesview: The text editor's text view.
		@type scribesview: A ScribesTextView object.
		"""
		self.scribesview = editor.textview
		self.editor = editor
		self.__manager = manager
		self.menu = None
		self.image = None
		self.bookmark_line_menuitem = None
		self.remove_bookmark_menuitem = None
		self.remove_all_bookmarks_menuitem = None
		self.next_bookmark_menuitem = None
		self.previous_bookmark_menuitem = None
		self.first_bookmark_menuitem = None
		self.last_bookmark_menuitem = None
		self.show_browser_menuitem = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		self.__signal_id_7 = None
		self.__signal_id_8 = None
		self.__signal_id_9 = None
		self.__signal_id_10 = None
		self.__signal_id_11 = None
		self.__signal_id_12 = None
		self.__signal_id_13 = None
		self.__signal_id_14 = None
		self.__signal_id_15 = None
		self.__signal_id_16 = None
		return

	def __create_widgets(self):
		"""
		Create menu items for the bookmarks menu.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.
		"""
		from gtk import Menu
		from SCRIBES.utils import create_image, create_menuitem
		from SCRIBES.info import scribes_data_folder
		image = scribes_data_folder + "/bookmarks.png"
		self.image = create_image(image)
		self.menu = Menu()
		from i18n import msg0013, msg0014
		from i18n import msg0015, msg0016, msg0017
		from i18n import msg0018, msg0019, msg0020
		self.bookmark_line_menuitem = create_menuitem(msg0013)
		self.remove_bookmark_menuitem = create_menuitem(msg0014)
		self.remove_all_bookmarks_menuitem = create_menuitem(msg0015)
		self.next_bookmark_menuitem = create_menuitem(msg0016)
		self.previous_bookmark_menuitem = create_menuitem(msg0017)
		self.first_bookmark_menuitem = create_menuitem(msg0018)
		self.last_bookmark_menuitem = create_menuitem(msg0019)
		self.show_browser_menuitem = create_menuitem(msg0020)
		return

	def __set_properties(self):
		"""
		Set the menu item's properties.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.
		"""
		self.set_image(self.image)
		self.set_submenu(self.menu)
		self.menu.append(self.bookmark_line_menuitem)
		self.menu.append(self.remove_bookmark_menuitem)
		self.menu.append(self.remove_all_bookmarks_menuitem)
		self.menu.append(self.next_bookmark_menuitem)
		self.menu.append(self.previous_bookmark_menuitem)
		self.menu.append(self.first_bookmark_menuitem)
		self.menu.append(self.last_bookmark_menuitem)
		self.menu.append(self.show_browser_menuitem)
		if self.editor.is_readonly:
			self.set_property("sensitive", False)
		return

	def __popup_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if menuitem == self.show_browser_menuitem:
			self.editor.triggermanager.trigger("show_bookmark_browser")
		elif menuitem == self.bookmark_line_menuitem:
			self.editor.triggermanager.trigger("bookmark_line")
		elif menuitem == self.remove_bookmark_menuitem:
			self.editor.triggermanager.trigger("remove_bookmark")
		elif menuitem == self.remove_all_bookmarks_menuitem:
			self.editor.triggermanager.trigger("remove_all_bookmarks")
		elif menuitem == self.next_bookmark_menuitem:
			self.editor.triggermanager.trigger("next_bookmark")
		elif menuitem == self.previous_bookmark_menuitem:
			self.editor.triggermanager.trigger("previous_bookmark")
		elif menuitem == self.first_bookmark_menuitem:
			self.editor.triggermanager.trigger("first_bookmark")
		elif menuitem == self.last_bookmark_menuitem:
			self.editor.triggermanager.trigger("last_bookmark")
		return True

	def __popup_map_event_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@param event: An event that occurs when popup menu is displayed.
		@type event: A gtk.Event object.
		"""
		self.__sensitize_menuitem(menuitem)
		return True

	def __popup_map_event2_cb(self, menuitem, event):
		"""
		Handles callback when the "map-event" signal is emitted.

		@param self: Reference to the BookmarkPopupMenuItem instance.
		@type self: A BookmarkPopupMenuItem object.

		@param menuitem: The popup menu's menuitem.
		@type menuitem: A gtk.MenuItem object.

		@param event: An event that occurs when popup menu is displayed.
		@type event: A gtk.Event object.
		"""
		self.__sensitize_menuitem(menuitem)
		return True

	def __sensitize_menuitem(self, menuitem):
		menuitem.set_property("sensitive", False)
		try:
			self.__manager.is_initialized
			lines = self.__manager.get_bookmarked_lines()
			if lines:
				menuitem.set_property("sensitive", True)
		except:
			pass
		return

	def __popup_destroy_cb(self, textview, event):
		if self.__signal_id_1 and self.bookmark_line_menuitem.handler_is_connected(self.__signal_id_1):
			self.bookmark_line_menuitem.disconnect(self.__signal_id_1)
		if self.__signal_id_2 and self.remove_bookmark_menuitem.handler_is_connected(self.__signal_id_2):
			self.remove_bookmark_menuitem.disconnect(self.__signal_id_2)
		if self.__signal_id_3 and self.remove_bookmark_menuitem.handler_is_connected(self.__signal_id_3):
			self.remove_bookmark_menuitem.disconnect(self.__signal_id_3)
		if self.__signal_id_4 and self.remove_all_bookmarks_menuitem.handler_is_connected(self.__signal_id_4):
			self.remove_all_bookmarks_menuitem.disconnect(self.__signal_id_4)
		if self.__signal_id_5 and self.remove_all_bookmarks_menuitem.handler_is_connected(self.__signal_id_5):
			self.remove_all_bookmarks_menuitem.disconnect(self.__signal_id_5)
		if self.__signal_id_6 and self.next_bookmark_menuitem.handler_is_connected(self.__signal_id_6):
			self.next_bookmark_menuitem.disconnect(self.__signal_id_6)
		if self.__signal_id_7 and self.next_bookmark_menuitem.handler_is_connected(self.__signal_id_7):
			self.next_bookmark_menuitem.disconnect(self.__signal_id_7)
		if self.__signal_id_8 and self.previous_bookmark_menuitem.handler_is_connected(self.__signal_id_8):
			self.previous_bookmark_menuitem.disconnect(self.__signal_id_8)
		if self.__signal_id_9 and self.previous_bookmark_menuitem.handler_is_connected(self.__signal_id_9):
			self.previous_bookmark_menuitem.disconnect(self.__signal_id_9)
		if self.__signal_id_10 and self.first_bookmark_menuitem.handler_is_connected(self.__signal_id_10):
			self.first_bookmark_menuitem.disconnect(self.__signal_id_10)
		if self.__signal_id_11 and self.first_bookmark_menuitem.handler_is_connected(self.__signal_id_11):
			self.first_bookmark_menuitem.disconnect(self.__signal_id_11)
		if self.__signal_id_12 and self.last_bookmark_menuitem.handler_is_connected(self.__signal_id_12):
			self.last_bookmark_menuitem.disconnect(self.__signal_id_12)
		if self.__signal_id_13 and self.last_bookmark_menuitem.handler_is_connected(self.__signal_id_13):
			self.last_bookmark_menuitem.disconnect(self.__signal_id_13)
		if self.__signal_id_14 and self.show_browser_menuitem.handler_is_connected(self.__signal_id_14):
			self.show_browser_menuitem.disconnect(self.__signal_id_14)
		if self.__signal_id_15 and self.show_browser_menuitem.handler_is_connected(self.__signal_id_15):
			self.show_browser_menuitem.disconnect(self.__signal_id_15)
		if self.__signal_id_16 and self.scribesview.handler_is_connected(self.__signal_id_16):
			self.scribesview.disconnect(self.__signal_id_16)
		if self.bookmark_line_menuitem:
			self.bookmark_line_menuitem.destroy()
		if self.remove_bookmark_menuitem:
			self.remove_bookmark_menuitem.destroy()
		if self.remove_all_bookmarks_menuitem:
			self.remove_all_bookmarks_menuitem.destroy()
		if self.next_bookmark_menuitem:
			self.next_bookmark_menuitem.destroy()
		if self.previous_bookmark_menuitem:
			self.previous_bookmark_menuitem.destroy()
		if self.first_bookmark_menuitem:
			self.first_bookmark_menuitem.destroy()
		if self.last_bookmark_menuitem:
			self.last_bookmark_menuitem.destroy()
		if self.show_browser_menuitem:
			self.show_browser_menuitem.destroy()
		if self.menu:
			self.menu.destroy()
		if self.image:
			self.image.destroy()
		self.destroy()
		del self.scribesview, self.editor, self.bookmark_line_menuitem
		del self.remove_bookmark_menuitem, self.remove_all_bookmarks_menuitem
		del self.next_bookmark_menuitem, self.previous_bookmark_menuitem
		del self.first_bookmark_menuitem, self.last_bookmark_menuitem
		del self.show_browser_menuitem, self.menu, self.image, self.__manager
		del self.__signal_id_1, self.__signal_id_2, self.__signal_id_3
		del self.__signal_id_4, self.__signal_id_5, self.__signal_id_6
		del self.__signal_id_7, self.__signal_id_8, self.__signal_id_9
		del self.__signal_id_10, self.__signal_id_11, self.__signal_id_12
		del self.__signal_id_13, self.__signal_id_14, self.__signal_id_15
		del self.__signal_id_16, self
		self = None
		return
