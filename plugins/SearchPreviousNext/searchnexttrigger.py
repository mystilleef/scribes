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
This modules documents a class that creates a trigger to that searches
for text in the buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class SearchNextTrigger(object):
	"""
	This class implements an object that searches for text in the buffer.
	"""

	def __init__(self, editor):
		"""
		Initialize the trigger object.

		@param self: Reference to the SearchNextTrigger instance.
		@type self: A SearchNextTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__trigger.connect("activate", self.__search_next_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the SearchNextTrigger instance.
		@type self: A SearchNextTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__searcher = None
		return

	def __create_trigger(self):
		"""
		Create trigger.

		@param self: Reference to the SearchNextTrigger instance.
		@type self: A SearchNextTrigger object.
		"""
		# Trigger that searches for text.
		from trigger import Trigger
		self.__trigger = Trigger("search_next")
		self.__editor.triggermanager.add_trigger(self.__trigger, "control - g")
		return

	def __search_next_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SearchNextTrigger instance.
		@type self: A SearchNextTrigger object.

		@param trigger: Trigger that searches for next text.
		@type trigger: A Trigger object.
		"""
		try:
			self.__searcher.next()
		except AttributeError:
			from searchnext import SearchNext
			self.__searcher = SearchNext(self.__editor)
			self.__searcher.next()
		return
