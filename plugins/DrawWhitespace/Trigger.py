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
This module documents a class that creates a trigger to show or hide
white spaces.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates an object, a trigger, that allows users to
	show or hide white spaces
	"""

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_draw_spaces_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		self.__trigger = self.__create_trigger()
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		# Trigger to toggle white space.
		self.__trigger = self.__editor.create_trigger("show_white_spaces", "alt - period")
		self.__editor.add_trigger(self.__trigger)
		return self.__trigger

	def __toggle_draw_spaces_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the symbol browser.
		@type trigger: A Trigger object.
		"""
		from DrawWhitespaceMetadata import get_value, set_value
		value = False if get_value() else True
		set_value(value)
		if value:
			icon = "yes"
			message = "Showing whitespace"
		else:
			icon = "no"
			message = "Hiding whitespace"
		self.__editor.update_status_message(message, icon, 7)
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Trigger instance.
		@type self: An Trigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return
