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
components of the document browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class DocumentManager(GObject):
	"""
	This class manages graphic user interface components of the document
	browser.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"update": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-browser": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize an instance of this class.

		@param self: Reference to the DocumentManager instance.
		@type self: A DocumentManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__arrange_widgets()
		self.__signal_id_1 = self.connect_after("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__close_button.connect("clicked", self.__manager_clicked_cb)
		self.__signal_id_3 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__signal_id_4 = self.connect("show-browser", self.__show_browser_cb)

	def show_browser(self):
		"""
		Show the bookmark browser.

		@param self: Reference to the DocumentManager instance.
		@type self: A DocumentManager object.
		"""
		self.emit("update")
		return

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the DocumentManager instance.
		@type self: A DocumentManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Window import BrowserWindow
		self.__window = BrowserWindow(self, editor)
		from Treeview import BrowserTreeView
		self.__treeview = BrowserTreeView(self, editor)
		from gtk import STOCK_CLOSE, Button
		self.__close_button = Button(stock=STOCK_CLOSE, use_underline=True)
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __arrange_widgets(self):
		"""
		Arrange graphic user interface components.

		@param self: Reference to the DocumentManager instance.
		@type self: A DocumentManager object.
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

		@param self: Reference to the DocumentManager instance.
		@type self: A DocumentManager object.

		@param manager: Reference to the DocumentManager instance.
		@type manager: A DocumentManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		from operator import truth
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self.__close_button)
		disconnect_signal(self.__signal_id_3, self.__treeview)
		disconnect_signal(self.__signal_id_4, self)
		if truth(self.__close_button):
			self.__close_button.destroy()
		delete_attributes(self)
		del self
		self = None
		return

	def __manager_clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the DocumentManager instance.
		@type self: An DocumentManager object.

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

	def __show_browser_cb(self, manager):
		self.__window.show_dialog()
		return
