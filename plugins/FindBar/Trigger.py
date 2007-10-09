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
This modules documents a class that creates a trigger to show the text
editor's findbar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class FindBarTrigger(GObject):
	"""
	This class implements an object that shows the text editor's findbar.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger object.

		@param self: Reference to the FindBarTrigger instance.
		@type self: A FindBarTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__findbar_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the FindBarTrigger instance.
		@type self: A FindBarTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__manager = None
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __create_trigger(self):
		"""
		Create trigger.

		@param self: Reference to the FindBarTrigger instance.
		@type self: A FindBarTrigger object.
		"""
		# Trigger to show the findbar.
		self.__trigger = self.__editor.create_trigger("show_findbar", "ctrl - f")
		self.__editor.add_trigger(self.__trigger)
		return

	def __findbar_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the FindBarTrigger instance.
		@type self: A FindBarTrigger object.

		@param trigger: Trigger to show the findbar.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.show_bar()
		except AttributeError:
			from Manager import FindBar
			self.__manager = FindBar(self.__editor)
			self.__manager.show_bar()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the FindBarTrigger instance.
		@type self: A FindBarTrigger object.

		@param trigger: Reference to the FindBarTrigger instance.
		@type trigger: A FindBarTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		from operator import truth
		if truth(self.__manager): self.__manager.emit("delete")
		del self
		self = None
		return
