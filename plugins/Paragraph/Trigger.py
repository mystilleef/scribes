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
This module documents a class that creates a trigger to perform paragraph
operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates triggers for paragraph operations.
	Operations:
		- select paragraph
		- move cursor to next paragraph
		- move cursor to previous paragraph
		- paragraph fill
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
		self.__signal_id_1 = self.__select_paragraph_trigger.connect("activate", self.__select_cb)
		self.__signal_id_2 = self.__next_paragraph_trigger.connect("activate", self.__next_cb)
		self.__signal_id_3 = self.__previous_paragraph_trigger.connect("activate", self.__previous_cb)
		self.__signal_id_4 = self.__reflow_paragraph_trigger.connect("activate", self.__reflow_cb)
		self.__signal_id_5 = editor.textview.connect_after("populate-popup", self.__popup_cb)

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
		self.__select_paragraph_trigger = None
		self.__next_paragraph_trigger = None
		self.__previous_paragraph_trigger = None
		self.__reflow_paragraph_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		return

	def __create_triggers(self):
		"""
		Create the trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		# Trigger to select paragraph.
		self.__select_paragraph_trigger = self.__editor.create_trigger("select_paragraph", "alt+p")
		self.__editor.add_trigger(self.__select_paragraph_trigger)

		# Trigger to move cursor to next paragraph.
		self.__next_paragraph_trigger = self.__editor.create_trigger("next_paragraph", "alt+Down")
		self.__editor.add_trigger(self.__next_paragraph_trigger)

		# Trigger to move cursor to previous paragraph.
		self.__previous_paragraph_trigger = self.__editor.create_trigger("previous_paragraph", "alt+Up")
		self.__editor.add_trigger(self.__previous_paragraph_trigger)

		# Trigger to reflow paragraph.
		self.__reflow_paragraph_trigger = self.__editor.create_trigger("reflow_paragraph", "alt+q")
		self.__editor.add_trigger(self.__reflow_paragraph_trigger)
		return

	def __select_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.select_paragraph()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.select_paragraph()
		return

	def __previous_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.previous_paragraph()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.previous_paragraph()
		return

	def __next_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.next_paragraph()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.next_paragraph()
		return

	def __reflow_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		self.__editor.instance_manager.block_response()
		try:
			self.__manager.reflow_paragraph()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.reflow_paragraph()
		self.__editor.instance_manager.unblock_response()
		return

	def __destroy(self):
		"""
		Destroy trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		triggers = [self.__reflow_paragraph_trigger, self.__previous_paragraph_trigger,
			self.__next_paragraph_trigger, self.__select_paragraph_trigger]
		self.__editor.disconnect_signal(self.__signal_id_1, self.__select_paragraph_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__next_paragraph_trigger)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__previous_paragraph_trigger)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__reflow_paragraph_trigger)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor.textview)
		self.__editor.remove_triggers(triggers)
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

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		from PopupMenuItem import PopupMenuItem
		menu.prepend(PopupMenuItem(self.__editor))
		menu.show_all()
		return False
