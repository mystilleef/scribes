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

class ComboBoxEntry(object):
	"""
	This class creates a comboboxentry for the remote dialog.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__signal_id_1 = self.__editor.recent_manager.connect("changed", self.__entry_changed_cb)
		self.__signal_id_2 = self.__entry.connect("changed", self.__changed_cb)
		self.__signal_id_3 = self.__entry.connect("activate", self.__activate_cb)
		self.__signal_id_4 = manager.connect("load-file", self.__load_file_cb)
		self.__signal_id_5 = manager.connect("destroy", self.__destroy_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)
		idle_add(self.__emit_error)

	def __init_attributes(self, editor, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__model = self.__create_model()
		self.__manager = manager
		self.__combo = manager.glade.get_widget("ComboBoxEntry")
		self.__entry = manager.glade.get_widget("Entry")
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

	def __set_properties(self):
		"""
		Set properties

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.
		"""
		self.__combo.set_property("model", self.__model)
		self.__combo.set_property("text-column", 0)
		return

	def __create_model(self):
		"""
		Create a model.

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.

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
		self.__combo.set_property("sensitive", False)
		self.__model.clear()
		recent_infos = self.__editor.recent_manager.get_items()
		for recent_info in recent_infos:
			uri = recent_info.get_uri()
			if uri.startswith("file://"): continue
			self.__model.append([uri])
		self.__combo.set_property("sensitive", True)
		self.__entry.grab_focus()
		return False

	def __load_uri(self):
		"""
		Load selected file(s)

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.
		"""
		self.__manager.emit("hide-window")
		encoding = self.__manager.encoding
		uri = self.__entry.get_text().strip()
		if not uri: return False
		self.__editor.open_files([uri], encoding)
		return False

	def __emit_error(self):
		"""
		Emit error signal when comboboxentry has no text fields.

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.
		"""
		value = True if self.__entry.get_text() else False
		self.__manager.emit("error", value)
		return False

	def __entry_changed_cb(self, recent_manager):
		"""
		Handles callback when the "changed", signal is emitted.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.

		@param recent_manager: The text editor's recent_manager.
		@type recent_manager: A gtk.RecentManager object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)
		return True

	def __changed_cb(self, *args):
		"""
		Handles callback when selection changes in file chooser.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__emit_error)
		return False

	def __activate_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.
		"""
		from gobject import idle_add
		idle_add(self.__load_uri)
		return False

	def __load_file_cb(self, *args):
		"""
		Handles callback when "load-file" signal is activated.

		@param self: Reference to the ComboBoxEntry instance.
		@type self: A ComboBoxEntry object.
		"""
		from gobject import idle_add
		idle_add(self.__load_uri)
		return False

	def __destroy_cb(self, entry):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the ScribesComboBoxEntry instance.
		@type self: A ScribesComboBoxEntry object.

		@param entry: Reference to the ScribesComboBoxEntry instance.
		@type entry: A ScribesComboBoxEntry object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.recent_manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__manager)
		self.__combo.destroy()
		del self
		self = None
		return
