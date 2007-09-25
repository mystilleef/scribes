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
This module documents a class that creates a trigger to undo or redo
text operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class UndoRedoTrigger(GObject):
	"""
	This class creates an object, a trigger, that undoes or redoes text
	operations.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the UndoRedoTrigger instance.
		@type self: A UndoRedoTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__undo_trigger.connect("activate", self.__undo_cb)
		self.__signal_id_3 = self.__redo_trigger.connect("activate", self.__redo_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the UndoRedoTrigger instance.
		@type self: A UndoRedoTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__undo_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the UndoRedoTrigger instance.
		@type self: A UndoRedoTrigger object.
		"""
		# Trigger to undo a text operation.
		from SCRIBES.Trigger import Trigger
		self.__undo_trigger = Trigger("undo_action", "ctrl - z")
		self.__editor.add_trigger(self.__undo_trigger)

		# Trigger to redo a text operation.
		self.__redo_trigger = Trigger("redo_action", "ctrl - Z")
		self.__editor.add_trigger(self.__redo_trigger)
		return

	def __undo_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the UndoRedoTrigger instance.
		@type self: A UndoRedoTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Prevent save operations when the text editor is in readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		if self.__editor.textbuffer.can_undo():
			self.__editor.textbuffer.undo()
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "undo")
			from SCRIBES.cursor import move_view_to_cursor
			move_view_to_cursor(self.__editor.textview)
		else:
			from i18n import msg0003
			self.__editor.feedback.update_status_message(msg0003, "fail")
		return

	def __redo_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the UndoRedoTrigger instance.
		@type self: A UndoRedoTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			#  Prevent save operations when the text editor is in readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		if self.__editor.textbuffer.can_redo():
			self.__editor.textbuffer.redo()
			from i18n import msg0004
			self.__editor.feedback.update_status_message(msg0004, "redo")
			from SCRIBES.cursor import move_view_to_cursor
			move_view_to_cursor(self.__editor.textview)
		else:
			from i18n import msg0005
			self.__editor.feedback.update_status_message(msg0005, "fail")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the UndoRedoTrigger instance.
		@type self: An UndoRedoTrigger object.

		@param trigger: Reference to the UndoRedoTrigger instance.
		@type trigger: A UndoRedoTrigger object.
		"""
		self.__editor.triggermanager.remove_trigger(self.__undo_trigger)
		self.__editor.triggermanager.remove_trigger(self.__redo_trigger)
		if self.__signal_id_1 and self.__undo_trigger.handler_is_connected(self.__signal_id_1):
			self.__undo_trigger.disconnect(self.__signal_id_1)
		if self.__signal_id_2 and self.handler_is_connected(self.__signal_id_2):
			self.disconnect(self.__signal_id_2)
		if self.__signal_id_3 and self.handler_is_connected(self.__signal_id_3):
			self.__redo_trigger.disconnect(self.__signal_id_3)
		del self.__editor, self.__undo_trigger, self.__redo_trigger
		del self.__signal_id_2, self.__signal_id_1, self.__signal_id_3
		del self
		self = None
		return
