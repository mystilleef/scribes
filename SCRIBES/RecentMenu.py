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
This module documents a class that implements a recent menu for the text
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import RecentChooserMenu

class RecentMenu(RecentChooserMenu):
	"""
	This class implements the recent menu for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the recent menu.

		@param self: Reference to the RecentMenu instance.
		@type self: A RecentMenu object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		RecentChooserMenu.__init__(self, editor.recent_manager)
		self.__set_properties()
		self.__signal_id_1 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = self.__editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = self.connect("item-activated", self.__recent_item_activated_cb)

	def __init_attributes(self, editor):
		"""
		The recent menu's data attributes.

		@param self: Reference to the RecentMenu instance.
		@type self: A RecentMenu object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__limit = 10
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__registration_id = editor.register_termination_id()
		return

	def __set_properties(self):
		"""
		Define the default properties of the menu.

		@param self: Reference to the RecentMenu instance.
		@type self: A RecentMenu object.
		"""
		from gtk import RECENT_SORT_MRU
		self.set_show_numbers(False)
		self.set_property("sort-type", RECENT_SORT_MRU)
		self.set_property("filter", self.__create_filter())
		self.set_property("limit", self.__limit)
		self.set_property("local-only", False)
		self.set_property("show-icons", True)
		self.set_property("show-not-found", False)
		self.set_property("show-tips", True)
		return

	def __create_filter(self):
		"""
		Create a filter for the recent menu.

		@param self: Reference to the RecentMenu instance.
		@type self: A RecentMenu object.

		@return: A filter for the recent menu.
		@rtype: A gtk.RecentFilter object.
		"""
		from gtk import RecentFilter
		recent_filter = RecentFilter()
		recent_filter.add_application("scribes")
		return recent_filter

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the RecentMenu.
		@type self: A RecentMenu object.
		"""
		from utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__editor)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self)
		# Unregister object so that editor can quit.
		self.destroy()
		self.__editor.unregister_termination_id(self.__registration_id)
		delete_attributes(self)
		# Delete data attributes.
		del self
		self = None
		return

	def __recent_item_activated_cb(self, recent_chooser):
		"""
		Handles callback when the "item-activated" signal is emitted.

		@param self: Reference to the RecentMenu instance.
		@type self: A RecentMenu object.

		@param recent_chooser: Reference to the RecentMenu.
		@type recent_chooser: A RecentMenu object.
		"""
		uri = self.get_current_uri()
		self.__editor.instance_manager.open_files([uri])
		return True

	def __close_document_cb(self, editor):
		self.__destroy()
		return
