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
This module documents a class that creates a triggers to select text
within pair characters.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class SearchTrigger(GObject):
	"""
	This class implements triggers to select text within pair characters.
	"""
	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the SearchTrigger instance.
		@type self: An SearchTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_triggers()
		self.__signal_id_1 = self.__next_trigger.connect("activate", self.__search_next_cb)
		self.__signal_id_2 = self.__previous_trigger.connect("activate", self.__search_previous_cb)
		self.__signal_id_3 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the SearchTrigger instance.
		@type self: A SearchTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__next_searcher = None
		self.__previous_searcher = None
		self.__next_trigger = self.__previous_trigger = None
		self.__signal_id_2 = self.__signal_id_1 = None
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __create_triggers(self):
		"""
		Create the trigger.

		@param self: Reference to the SearchTrigger instance.
		@type self: A SearchTrigger object.
		"""
		self.__next_trigger = self.__editor.create_trigger("search_next", "ctrl - g")
		self.__editor.add_trigger(self.__next_trigger)

		self.__previous_trigger = self.__editor.create_trigger("search_previous", "ctrl - G")
		self.__editor.add_trigger(self.__previous_trigger)
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the SearchTrigger instance.
		@type self: An SearchTrigger object.
		"""
		self.__editor.remove_trigger(self.__next_trigger)
		self.__editor.remove_trigger(self.__previous_trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__next_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__previous_trigger)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		del self
		self = None
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __search_next_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SearchTrigger instance.
		@type self: A SearchTrigger object.

		@param trigger: Trigger that searches for next text.
		@type trigger: A Trigger object.
		"""
		try:
			self.__next_searcher.next()
		except AttributeError:
			from Next import SearchNext
			self.__next_searcher = SearchNext(self, self.__editor)
			self.__next_searcher.next()
		return

	def __search_previous_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param trigger: Search for previous text in the buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__previous_searcher.previous()
		except AttributeError:
			from Previous import SearchPrevious
			self.__previous_searcher = SearchPrevious(self, self.__editor)
			self.__previous_searcher.previous()
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return
