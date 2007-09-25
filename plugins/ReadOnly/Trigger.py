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
This module documents a class that toggles readonly mode.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class ReadOnlyTrigger(GObject):
	"""
	This class creates an object, a trigger, that allows users to toggle
	readonly mode.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the ReadOnlyTrigger instance.
		@type self: A ReadOnlyTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_readonly_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the ReadOnlyTrigger instance.
		@type self: A ReadOnlyTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the ReadOnlyTrigger instance.
		@type self: A ReadOnlyTrigger object.
		"""
		# Trigger to save a file.
		from SCRIBES.Trigger import Trigger
		self.__trigger = Trigger("toggle_readonly", "F3")
		self.__editor.triggermanager.add_trigger(self.__trigger)
		return

	def __toggle_readonly_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ReadOnlyTrigger instance.
		@type self: A ReadOnlyTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.uri is None:
			# Do not toggle readonly mode when the editor contains no document.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		if self.__editor.is_readonly:
			from SCRIBES.utils import check_uri_permission
			result = check_uri_permission(self.__editor.uri)
			if result:
				self.__editor.emit("disable-readonly")
			else:
				from i18n import msg0002
				self.__editor.feedback.update_status_message(msg0002, "fail")
		else:
			if self.__editor.file_is_saved is False:
				self.__editor.triggermanager.trigger("save_file")
			self.__editor.emit("enable-readonly")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ReadOnlyTrigger instance.
		@type self: An ReadOnlyTrigger object.

		@param trigger: Reference to the ReadOnlyTrigger instance.
		@type trigger: A ReadOnlyTrigger object.
		"""
		self.__editor.triggermanager.remove_trigger(self.__trigger)
		if self.__signal_id_1 and self.__trigger.handler_is_connected(self.__signal_id_1):
			self.__trigger.disconnect(self.__signal_id_1)
		if self.__signal_id_2 and self.handler_is_connected(self.__signal_id_2):
			self.disconnect(self.__signal_id_2)
		del self.__editor, self.__trigger
		del self.__signal_id_2, self.__signal_id_1
		del self
		self = None
		return
