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
This module documents a class that creates a trigger to show the text
editor's print dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class PrintTrigger(GObject):
	"""
	This class implements an object that creates a trigger to show the
	text editor's print dialog.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_print_dialog_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the object's data attributes.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__print_dialog = None
		self.__trigger = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		return

	def __create_trigger(self):
		"""
		Creates a trigger to show the text editor's print dialog.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.
		"""
		# Trigger to show the print dialog.
		from SCRIBES.Trigger import Trigger
		self.__trigger = Trigger("show_print_dialog", "ctrl - p")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_print_dialog_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the PrintTrigger instance.
		@type self: A PrintTrigger object.

		@param trigger: A trigger to show the print dialog.
		@type trigger: A Trigger object.
		"""
		from Dialog import PrintDialog
		self.__print_dialog = PrintDialog(self.__editor)
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the destroy "signal" is emitted.

		@param self: Reference to the PrintDialogTrigger instance.
		@type self: An PrintDialogTrigger object.

		@param trigger: Reference to the PrintDialogTrigger instance.
		@type trigger: An PrintDialogTrigger object.
		"""
		self.__editor.triggermanager.remove_trigger(self.__trigger)
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__trigger)
		disconnect_signal(self.__signal_id_2, self)
		delete_attributes(self)
		del self
		self = None
		return
