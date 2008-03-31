# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This modules documents a class that monitors the changes in the use
tabs configuration dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class monitors the changes in the "use tabs" configuration
	database.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Reference to manager object.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__sig_id1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__send_activate_signal()

	def __init_attributes(self, editor, manager):
		"""
		Initialize attributes.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Reference to manager object.
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "UseTabs.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__sig_id1 = self.__monitor_id_1 = None
		return

	def __send_activate_signal(self):
		"""
		Send use tab value in database to object that needs them.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		from UseTabsMetadata import get_value
		self.__manager.emit("activate", get_value())
		return

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		"""
		Handles callback when the destroy signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__destroy()
		return

	def __database_changed_cb(self, *args):
		"""
		Handles callback when value in database changes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__send_activate_signal()
		return False
