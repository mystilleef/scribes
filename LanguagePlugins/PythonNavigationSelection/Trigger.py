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
This module documents a class that creates a trigger that allows users
to perform navigation and selection functions for python source code.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates objects, triggers,  that allows users to perform
	python specific navigation and selection operations in Python source
	code.
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
		self.__signal_id_1 = self.__prv_trigger.connect("activate", self.__prv_block_cb)
		self.__signal_id_2 = self.__nxt_trigger.connect("activate", self.__nxt_block_cb)
		self.__signal_id_3 = self.__select_trigger.connect("activate", self.__select_block_cb)
		self.__signal_id_4 = self.__end_trigger.connect("activate", self.__end_block_cb)
		self.__signal_id_5 = self.__select_function_trigger.connect("activate", self.__select_function_cb)
		self.__signal_id_6 = self.__select_class_trigger.connect("activate", self.__select_class_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__prv_trigger = self.__create_previous_block_trigger()
		self.__nxt_trigger = self.__create_next_block_trigger()
		self.__select_trigger = self.__create_select_block_trigger()
		self.__end_trigger = self.__create_end_block_trigger()
		self.__select_function_trigger = self.__create_select_function_trigger()
		self.__select_class_trigger = self.__create_select_class_trigger()
		self.__manager = None
		self.__signal_id_1 = None
		return

	def __create_previous_block_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		# Trigger to test python block detection.
		trigger = self.__editor.create_trigger("move_to_previous_block", "alt - bracketleft")
		self.__editor.add_trigger(trigger)
		return trigger

	def __create_next_block_trigger(self):
		# Trigger to test python block detection.
		trigger = self.__editor.create_trigger("move_to_next_block", "alt - bracketright")
		self.__editor.add_trigger(trigger)
		return trigger

	def __create_select_block_trigger(self):
		# Trigger to test python block detection.
		trigger = self.__editor.create_trigger("select_python_block", "alt - h")
		self.__editor.add_trigger(trigger)
		return trigger

	def __create_end_block_trigger(self):
		# Trigger to test python block detection.
		trigger = self.__editor.create_trigger("move_to_block_end", "alt - e")
		self.__editor.add_trigger(trigger)
		return trigger

	def __create_select_function_trigger(self):
		# Trigger to test python block detection.
		trigger = self.__editor.create_trigger("select_function", "alt - f")
		self.__editor.add_trigger(trigger)
		return trigger

	def __create_select_class_trigger(self):
		# Trigger to test python block detection.
		trigger = self.__editor.create_trigger("select_class", "alt - a")
		self.__editor.add_trigger(trigger)
		return trigger

	def __prv_block_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: Trigger that closes current window and reopens new one.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.previous_block()
		except:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.previous_block()
		return

	def __nxt_block_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: Trigger that closes current window and reopens new one.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.next_block()
		except:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.next_block()
		return

	def __select_function_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: Trigger that closes current window and reopens new one.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.select_function()
		except:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.select_function()
		return

	def __select_class_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: Trigger that closes current window and reopens new one.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.select_class()
		except:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.select_class()
		return

	def __select_block_cb(self, *args):
		try:
			self.__manager.select_block()
		except:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.select_block()
		return

	def __end_block_cb(self, *args):
		try:
			self.__manager.end_of_block()
		except:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.end_of_block()
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Trigger instance.
		@type self: An Trigger object.
		"""
		self.__editor.remove_trigger(self.__prv_trigger)
		self.__editor.remove_trigger(self.__nxt_trigger)
		self.__editor.remove_trigger(self.__select_trigger)
		self.__editor.remove_trigger(self.__end_trigger)
		self.__editor.remove_trigger(self.__select_function_trigger)
		self.__editor.remove_trigger(self.__select_class_trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__prv_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__nxt_trigger)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__select_trigger)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__end_trigger)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__select_function_trigger)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__select_class_trigger)
		if self.__manager: self.__manager.destroy()
		del self
		self = None
		return
