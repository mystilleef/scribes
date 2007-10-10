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
This module documents a class that creates a trigger to scroll the
view up or down or center it.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates triggers for scroll navigation.
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
		self.__create_triggers()
		self.__signal_id_1 = self.__up_trigger.connect("activate", self.__up_cb)
		self.__signal_id_2 = self.__down_trigger.connect("activate", self.__down_cb)
		self.__signal_id_3 = self.__middle_trigger.connect("activate", self.__middle_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None
		self.__up_trigger = None
		self.__down_trigger = None
		self.__middle_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		return

	def __create_triggers(self):
		"""
		Create the trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		# Trigger to scroll up.
		self.__up_trigger = self.__editor.create_trigger("scroll_up", "ctrl - Up")
		self.__editor.add_trigger(self.__up_trigger)

		# Trigger to scroll down.
		self.__down_trigger = self.__editor.create_trigger("scroll_down", "ctrl - Down")
		self.__editor.add_trigger(self.__down_trigger)

		# Trigger to center current line.
		self.__middle_trigger = self.__editor.create_trigger("center", "alt - m")
		self.__editor.add_trigger(self.__middle_trigger)
		return

	def __up_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.scroll_up()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.scroll_up()
		return

	def __down_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.scroll_down()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.scroll_down()
		return

	def __middle_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.center()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.center()
		return

	def __destroy(self):
		"""
		Destroy trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__up_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__down_trigger)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__middle_trigger)
		self.__editor.remove_trigger(self.__up_trigger)
		self.__editor.remove_trigger(self.__down_trigger)
		self.__editor.remove_trigger(self.__middle_trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return

	def destroy(self):
		"""
		Destroy trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		self.__destroy()
		return
