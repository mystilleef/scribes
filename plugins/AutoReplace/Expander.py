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
This module documents a class that expands abbreviations the editor's
buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class AutoReplaceExpander(object):
	"""
	This class creates an object that expands abbreviations in the
	buffer.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the monitor object.

		@param self: Reference to the AutoReplaceExpander instance.
		@type self: An AutoReplaceExpander object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.
		"""
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = self.__manager.connect("abbreviations-updated", self.__expander_abbreviations_updated_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__expander_destroy_cb)
		self.__signal_id_3 = self.__manager.connect("abbreviation-found", self.__expander_abbreviation_found_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the AutoReplaceExpander instance.
		@type self: An AutoReplaceExpander object.

		@param manager: Reference to the AutoReplaceManager
		@type manager: An AutoReplaceManager object.
		"""
		# Reference to the AutoReplaceManager.
		self.__manager = manager
		# Reference to the editor.
		self.__editor = editor
		# A dictionary of abbreviations.
		self.__abbreviation_dictionary = {}
		# Identifier for the "abbreviations-updated" signal.
		self.__signal_id_1 = None
		# Identifier for the "destroy" signal.
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __expander_abbreviations_updated_cb(self, manager, abbreviation_dictionary):
		"""
		Handles callback when the "abbreviations-updated" signal is
		emitted.

		@param self: Reference to the AutoReplaceMonitor instance.
		@type self: An AutoReplaceMonitor object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.

		@param abbreviation_dictionary: A dictionary of abbreviations.
		@type abbreviation_dictionary: A Dictionary object.
		"""
		self.__abbreviation_dictionary = abbreviation_dictionary
		return

	def __expander_destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.
		"""
		self.__abbreviation_dictionary.clear()
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__manager)
		del self
		self = None
		return

	def __expander_abbreviation_found_cb(self, manager, abbreviation):
		"""
		Handles callback when the "abbreviation-found" signal is emitted.

		@param self: Reference to the AutoReplaceExpander instance.
		@type self: An AutoReplaceExpander object.

		@param monitor: Reference to the AutoReplaceManager.
		@type monitor: An AutoReplaceManager object.

		@param abbreviation: An abbreviation eligible for replacement.
		@type abbreviation: A String object.
		"""
		try:
			expanded_word = self.__abbreviation_dictionary[abbreviation[:-1]]
		except KeyError:
			return
		delimeter_character = abbreviation[-1]
		iterator = self.__editor.get_cursor_iterator()
		tmp_iterator = iterator.copy()
		for value in range(len(abbreviation[:-1])):
			tmp_iterator.backward_char()
		self.__editor.textbuffer.delete(tmp_iterator, iterator)
		self.__editor.textbuffer.insert_at_cursor(expanded_word + delimeter_character)
		from i18n import msg0001
		message = msg0001  % (abbreviation[:-1], expanded_word)
		self.__editor.feedback.update_status_message(message, "succeed")
		return
