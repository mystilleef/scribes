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
This modules documents a class that implements a "fork scribes" check
button for the advanced configuration window.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class CheckButton(object):
	"""
	This class creates an object that defines the behavior of the
	"fork scribes" check button.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the CheckButton instance.
		@type self: A CheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages components
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sig_id1 = self.__button.connect("toggled", self.__toggled_cb)
		self.__sig_id2 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		"""
		Initialize object attributes.

		@param self: Reference to the CheckButton instance.
		@type self: A CheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages components
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.glade.get_widget("ForkScribesCheckButton")
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "ForkScribes.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__sig_id1 = self.__monitor_id_1 = None
		return

	def __set_properties(self):
		"""
		Set default properties of the check button.

		@param self: Reference to the CheckButton instance.
		@type self: A CheckButton object.
		"""
		from ForkScribesMetadata import get_value
		self.__button.set_active(get_value())
		return

	def __destroy(self):
		"""
		Destroy this object.

		@param self: Reference to the CheckButton instance.
		@type self: A CheckButton object.
		"""
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		self.__editor.disconnect_signal(self.__sig_id1, self.__button)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __toggled_cb(self, *args):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ForkScribesCheckButton instance.
		@type self: A ForkScribesCheckButton object.
		"""
		from ForkScribesMetadata import set_value
		fork_scribes = True if self.__button.get_active() else False
		set_value(fork_scribes)
		return True

	def __destroy_cb(self, *args):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the CheckButton instance.
		@type self: A CheckButton object.
		"""
		self.__destroy()
		return False

	def __database_changed_cb(self, *args):
		"""
		Handles callback when configuration database changes.

		@param self: Reference to the CheckButton instance.
		@type self: A CheckButton object.
		"""
		self.__button.handler_block(self.__sig_id1)
		from ForkScribesMetadata import get_value
		fork_scribes = get_value()
		if fork_scribes and self.__button.get_active() is False:
			self.__button.set_active(True)
		if fork_scribes is False and self.__button.get_active():
			self.__button.set_active(False)
		self.__button.handler_unblock(self.__sig_id1)
		return
