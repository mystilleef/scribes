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
This module documents a class manages recently used files for the text
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class RecentManager(object):
	"""
	This class creates an object that manages recently used files for
	the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = self.__editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = self.__editor.connect("loaded-document", self.__recent_loaded_document_cb)
		self.__signal_id_4 = self.__editor.connect("renamed-document", self.__recent_renamed_document_cb)

	def __call__(self):
		"""
		Return a recent manager.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.

		@return: A recent manager.
		@rtype: A gtk.RecentManager object.
		"""
		return self.__manager

	def __init_attributes(self, editor):
		"""
		Initialize the manager's data attributes.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = self.__create_recent_manager()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__registration_id = editor.register_termination_id()
		return

	def __create_recent_manager(self):
		"""
		Create a recent manager for the text editor.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.
		"""
		from gtk import recent_manager_get_default
		manager = recent_manager_get_default()
		return manager

	def __create_recent_data(self, uri):
		"""
		Create a metadata information for a recently opened file.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.

		@param uri: Reference to a file.
		@type uri: A String object.

		@return: A dictionary containing information about a file.
		@rtype: A Dictionary object.
		"""
		from gnomevfs import get_mime_type, URI
		mime_type = get_mime_type(self.__editor.uri)
		app_name = "scribes"
		app_exec = "%U"
		display_name = URI(self.__editor.uri).short_name
		description = "A text file."
		recent_data = {
				"mime_type": mime_type,
				"app_name": app_name,
				"app_exec": app_exec,
				"display_name": display_name,
				"description": description,
			}
		return recent_data

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the RecentManager.
		@type self: A RecentManager object.
		"""
		from utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__editor)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self.__editor)
		disconnect_signal(self.__signal_id_4, self.__editor)
		# Unregister object so that editor can quit.
		self.__editor.unregister_termination_id(self.__registration_id)
		delete_attributes(self)
		# Delete data attributes.
		del self
		self = None
		return

	def __recent_loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager.add_full(uri, self.__create_recent_data(uri))
		return

	def __recent_renamed_document_cb(self, editor, uri):
		"""
		Handles callback when the "renamed-document" signal is emitted.

		@param self: Reference to the RecentManager instance.
		@type self: A RecentManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager.add_full(uri, self.__create_recent_data(uri))
		return

	def __close_document_cb(self, editor):
		self.__destroy()
		return
