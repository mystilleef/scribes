# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
This module documents a class that manages graphic user interface
components of the bookmark browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class BookmarkManager(GObject):
	"""
	This class manages graphic user interface components of the bookmark
	browser.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"update": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize an instance of this class.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__arrange_widgets()
		self.__signal_id_1 = self.connect_after("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__close_button.connect("clicked", self.__manager_clicked_cb)
		self.__signal_id_3 = self.__treeview.connect("row-activated", self.__row_activated_cb)

	def show_browser(self):
		"""
		Show the bookmark browser.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		self.emit("update")
		self.__window.show_dialog()
		return

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Window import BookmarkWindow
		self.__window = BookmarkWindow(self, editor)
		from Treeview import BookmarkTreeView
		self.__treeview = BookmarkTreeView(self, editor)
		from gtk import STOCK_CLOSE, Button
		self.__close_button = Button(stock=STOCK_CLOSE, use_underline=True)
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

	def __arrange_widgets(self):
		"""
		Arrange graphic user interface components.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		from SCRIBES.utils import create_scrollwin
		scrollwin = create_scrollwin()
		scrollwin.add(self.__treeview)
		self.__window.main_area.pack_start(scrollwin, True, True, 0)
		self.__window.button_area.pack_start(self.__close_button, False, False, 0)
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.
		"""
		if self.__signal_id_1 and self.handler_is_connected(self.__signal_id_1):
			self.disconnect(self.__signal_id_1)
		if self.__signal_id_2 and self.__close_button.handler_is_connected(self.__signal_id_2):
			self.__close_button.disconnect(self.__signal_id_2)
		if self.__signal_id_3 and self.__treeview.handler_is_connected(self.__signal_id_3):
			self.__treeview.disconnect(self.__signal_id_3)
		self.__close_button.destroy()
		del self.__editor, self.__window, self.__treeview, self.__signal_id_1
		del self.__close_button, self.__signal_id_2
		del self
		self = None
		return

	def __manager_clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the BookmarkManager instance.
		@type self: An BookmarkManager object.

		@param button: Reference to the close button.
		@type button: A gtk.Button object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__window.hide_dialog()
		return False

	def __row_activated_cb(self, *args):
		self.__window.hide_dialog()
		return False
