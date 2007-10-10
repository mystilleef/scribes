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
This module documents a class that creates a trigger to shows or hides
the toolbar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class ToggleTrigger(GObject):
	"""
	This class creates an object, a trigger, that shows or hides the
	toolbar and status area.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the ToggleTrigger instance.
		@type self: A ToggleTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_toolbar_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the ToggleTrigger instance.
		@type self: A ToggleTrigger object.

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

		@param self: Reference to the ToggleTrigger instance.
		@type self: A ToggleTrigger object.
		"""
		# Trigger to show or hide toolbar.
		self.__trigger = self.__editor.create_trigger("toggle_minimal_interface", "ctrl - alt - m")
		self.__editor.add_trigger(self.__trigger)
		return

	def __toggle_toolbar_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ToggleTrigger instance.
		@type self: A ToggleTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		from gconf import client_get_default
		client = client_get_default()
		from operator import contains
		if contains((self.__editor.toolbar.is_visible, self.__editor.statuscontainer.is_visible), True):
			# Hide the toolbar and status area.
			client.set_bool("/apps/scribes/hide_toolbar", True)
			client.set_bool("/apps/scribes/hide_status_area", True)
		else:
			# Hide the toolbar and status area.
			client.set_bool("/apps/scribes/hide_toolbar", False)
			client.set_bool("/apps/scribes/hide_status_area", False)
		client.notify("/apps/scribes/hide_status_area")
		client.notify("/apps/scribes/hide_toolbar")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ToggleTrigger instance.
		@type self: An ToggleTrigger object.

		@param trigger: Reference to the ToggleTrigger instance.
		@type trigger: A ToggleTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		del self
		self = None
		return
