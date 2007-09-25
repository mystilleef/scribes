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

from SCRIBES.sdialog import Dialog

class BookmarkWindow(Dialog):
	"""
	This class creates the window for the bookmark browser window.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize an instance of this class.

		@param self: Reference to the BookmarkWindow instance.
		@type self: A BookmarkWindow object.

		@param manager: Reference to the BookmarkManager instance
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Dialog.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id = self.__manager.connect("destroy", self.__window_destroy_cb)
		self.__signal_id_1 = self.__editor.store.connect("updated", self.__store_updated_cb)

	def show_dialog(self):
		"""
		Show the bookmark browser.

		@param self: Reference to the BookmarkWindow instance.
		@type self: A BookmarkWindow object.
		"""
		try:
			if not self.__bookmark_manager:
				raise AttributeError
			lines = self.__bookmark_manager.get_bookmarked_lines()
			if not lines:
				raise AttributeError
		except AttributeError:
			from i18n import msg0005
			self.__editor.feedback.update_status_message(msg0005, "warning")
			return
		self.__editor.emit("show-dialog", self)
		from i18n import msg0001
		self.__status_id = self.__editor.feedback.set_modal_message(msg0001, "info")
		Dialog.show_dialog(self)
		return

	def hide_dialog(self):
		"""
		Hide the bookmark browser.

		@param self: Reference to the BookmarkWindow instance.
		@type self: A BookmarkWindow object.
		"""
		self.__editor.emit("hide-dialog", self)
		self.__editor.feedback.unset_modal_message(self.__status_id)
		Dialog.hide_dialog(self)
		return

	def __window_destroy_cb(self, manager):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the BookmarkWindow instance.
		@type self: An BookmarkWindow object.

		@param manager: Reference to the BookmarkManager.
		@type manager: An BookmarkManager object.
		"""
		if self.__signal_id and self.__manager.handler_is_connected(self.__signal_id):
			self.__manager.disconnect(self.__signal_id)
		if self.__signal_id_1 and self.__editor.store.handler_is_connected(self.__signal_id_1):
			self.__editor.store.disconnect(self.__signal_id_1)
		self.destroy()
		del self.__editor, self.__signal_id, self.__signal_id_1, self.__manager
		del self.__status_id, self.__bookmark_manager, self
		self = None
		return

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BookmarkWindow instance.
		@type self: A BookmarkWindow object.

		@param manager: Reference to the BookmarkManager instance
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__signal_id = None
		self.__signal_id_1 = None
		self.__status_id = None
		self.__bookmark_manager = editor.store.get_object("BookmarkManager")
		return

	def __set_properties(self):
		"""
		Define the default behavior of the dialog.

		@param self: Reference to the BookmarkWindow instance.
		@type self: A BookmarkWindow object.
		"""
		self.set_property("name", "scribes bookmark browser dialog")
		from i18n import msg0002
		self.set_property("title", msg0002)
		from SCRIBES.utils import calculate_resolution_independence
		width, height = calculate_resolution_independence(self.__editor.window, 1.679790026, 1.865209472)
		self.set_property("default-width", width)
		self.set_property("default-height", height)
		self.set_transient_for(self.__editor.window)
		return

	def __store_updated_cb(self, store, name):
		"""
		Handles callback when the "updated" signal is emitted.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@param store: Reference to a Store object.
		@type store: A Store object.

		@param name: The name of the object that was updated.
		@type name: A String object.
		"""
		if name in ["BookmarkManager"]:
			if self.__editor.store:
				self.__bookmark_manager = self.__editor.store.get_object("BookmarkManager")
		return
