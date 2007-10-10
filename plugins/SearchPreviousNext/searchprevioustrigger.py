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
This modules documents a class that creates a trigger to search for
previous text in the buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class SearchPreviousTrigger(object):
	"""
	This class implements an object that searches for previous text in
	buffer.
	"""

	def __init__(self, editor):
		"""
		Initialize the trigger object.

		@param self: Reference to the SearchPreviousTrigger instance.
		@type self: A SearchPreviousTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__trigger.connect("activate", self.__search_previous_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the SearchPreviousTrigger instance.
		@type self: A SearchPreviousTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__search_previous = None
		return

	def __create_trigger(self):
		"""
		Create trigger.

		@param self: Reference to the SearchPreviousTrigger instance.
		@type self: A SearchPreviousTrigger object.
		"""
		# Trigger to search for previous text in the buffer.
		self.__trigger = self.__editor.create_trigger("search_previous")
		self.__editor.add_trigger(self.__trigger, "control - G")
		return

	def __search_previous_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SearchPreviousTrigger instance.
		@type self: A SearchPreviousTrigger object.

		@param trigger: Search for previous text in the buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__search_previous.previous()
		except AttributeError:
			from searchprevious import SearchPrevious
			self.__search_previous = SearchPrevious(self.__editor)
			self.__search_previous.previous()
		return
