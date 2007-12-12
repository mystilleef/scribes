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
This module documents a class that creates the window for the document
browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Dialog

class BrowserWindow(Dialog):
	"""
	This class creates the window for the document browser window.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize an instance of this class.

		@param self: Reference to the BrowserWindow instance.
		@type self: A BrowserWindow object.

		@param manager: Reference to the BookmarkManager instance
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Dialog.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id = self.__manager.connect("destroy", self.__window_destroy_cb)
		self.__signal_id_1 = self.connect("close", self.__close_cb)
		self.__signal_id_2 = self.connect("response", self.__close_cb)

	def show_dialog(self):
		"""
		Show the document browser.

		@param self: Reference to the BrowserWindow instance.
		@type self: A BrowserWindow object.
		"""
		self.__editor.emit("show-dialog", self)
		from i18n import msg0001
		self.__status_id = self.__editor.feedback.set_modal_message(msg0001, "open")
		self.show_all()
		self.run()
		return

	def hide_dialog(self):
		"""
		Hide the document browser.

		@param self: Reference to the BrowserWindow instance.
		@type self: A BrowserWindow object.
		"""
		self.__editor.emit("hide-dialog", self)
		self.__editor.feedback.unset_modal_message(self.__status_id)
		self.hide()
		return

	def __close_cb(self, *args):
		self.hide_dialog()
		return False

	def __window_destroy_cb(self, manager):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the BrowserWindow instance.
		@type self: An BrowserWindow object.

		@param manager: Reference to the BookmarkManager.
		@type manager: An BookmarkManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		del self
		self = None
		return

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BrowserWindow instance.
		@type self: A BrowserWindow object.

		@param manager: Reference to the BookmarkManager instance
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__signal_id = self.__signal_id_1 = self.__signal_id_2 = None
		self.__status_id = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the dialog.

		@param self: Reference to the BrowserWindow instance.
		@type self: A BrowserWindow object.
		"""
		self.set_property("name", "DocumentBrowserDialog")
		from i18n import msg0002
		self.set_property("title", msg0002)
		width, height = self.__editor.calculate_resolution_independence(self.__editor.window, 1.6, 2.5)
		self.set_property("default-width", width)
		self.set_property("default-height", height)
		self.set_transient_for(self.__editor.window)
		self.set_property("has-separator", False)
		self.set_property("skip-pager-hint", True)
		self.set_property("skip-taskbar-hint", True)
		self.set_property("urgency-hint", False)
		self.set_property("modal", True)
		from gtk import WIN_POS_CENTER_ON_PARENT
		self.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		self.set_property("resizable", True)		
		self.set_keep_above(True)
		return
