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
This module documents a class that creates a trigger for the text
editor's remote dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class RemoteDialogTrigger(object):
	"""
	This class creates an object that shows the text editor's remote
	dialog.
	"""

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the RemoteDialogTrigger instance.
		@type self: An RemoteDialogTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_remote_dialog_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the RemoteDialogTrigger instance.
		@type self: A RemoteDialogTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__remote_dialog = None
		self.__trigger = None
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the RemoteDialogTrigger instance.
		@type self: A RemoteDialogTrigger object.
		"""
		# Trigger to show the remote dialog.
		self.__trigger = self.__editor.create_trigger("show_remote_dialog", "ctrl+l")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_remote_dialog_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the RemoteDialogTrigger instance.
		@type self: A RemoteDialogTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__remote_dialog.show_dialog()
		except AttributeError:
			from Manager import Manager
			self.__remote_dialog = Manager(self.__editor)
		return

	def destroy(self):
		"""
		Handles callback when the destroy "signal" is emitted.

		@param self: Reference to the OpenDialogTrigger instance.
		@type self: An OpenDialogTrigger object.

		@param trigger: Reference to the OpenDialogTrigger instance.
		@type trigger: An OpenDialogTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		if self.__remote_dialog: self.__remote_dialog.destroy()
		del self
		self = None
		return
