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
This module exposes a class that creates a comboboxentry for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ComboBoxEntry
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class ScribesComboBoxEntry(ComboBoxEntry):
	"""
	This class creates a comboboxentry for the text editor.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the comboboxentry object.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.
		"""
		ComboBoxEntry.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__populate_model()
		self.__signal_id_1 = self.__editor.recent_manager.connect("changed", self.__entry_changed_cb)
		self.__signal_id_2 = self.connect("delete", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the comboboxentry's attributes

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__model = self.__create_model()
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default properties on the comboboxentry.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.
		"""
		self.set_property("model", self.__model)
		self.set_property("text-column", 0)
		return

	def __create_model(self):
		"""
		Create a model.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.

		@return: A model for the ComboBoxEntry
		@rtype: A ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(str)
		return model

	def __populate_model(self):
		"""
		Populate the entry's model.

		The model should contain a list of remote URIs.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.
		"""
		self.__model.clear()
		recent_infos = self.__editor.recent_manager.get_items()
		for recent_info in recent_infos:
			uri = recent_info.get_uri()
			if uri.startswith("file://"):
				continue
			self.__model.append([uri])
		return

	def __entry_changed_cb(self, recent_manager):
		"""
		Handles callback when the "changed", signal is emitted.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.

		@param recent_manager: The text editor's recent_manager.
		@type recent_manager: A gtk.RecentManager object.
		"""
		self.__populate_model()
		return True

	def __destroy_cb(self, entry):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.

		@param entry: Reference to the ScribesComboBoxEntry instance.
		@type entry: A ScribesComboBoxEntry object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__editor.recent_manager)
		disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
