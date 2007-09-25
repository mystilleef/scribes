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
This module documents a class that creates a trigger that toggles spell
checking.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class SpellCheckTrigger(GObject):
	"""
	This class creates an object, a trigger, that toggles spell
	checking.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the SpellCheckTrigger instance.
		@type self: A SpellCheckTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_spell_checking_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the SpellCheckTrigger instance.
		@type self: A SpellCheckTrigger object.

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

		@param self: Reference to the SpellCheckTrigger instance.
		@type self: A SpellCheckTrigger object.
		"""
		# Trigger to toggle spell checking.
		from SCRIBES.Trigger import Trigger
		self.__trigger = Trigger("toggle_spell_checking", "F6")
		self.__editor.add_trigger(self.__trigger)
		return

	def __toggle_spell_checking_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SpellCheckTrigger instance.
		@type self: A SpellCheckTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		from gconf import client_get_default
		client = client_get_default()
		value = client.get_bool("/apps/scribes/spell_check")
		if value:
			client.set_bool("/apps/scribes/spell_check", False)
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "warning")
		else:
			client.set_bool("/apps/scribes/spell_check", True)
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "succeed")
		client.notify("/apps/scribes/spell_check")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SpellCheckTrigger instance.
		@type self: An SpellCheckTrigger object.

		@param trigger: Reference to the SpellCheckTrigger instance.
		@type trigger: A SpellCheckTrigger object.
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
