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

class BracketSelectionTrigger(object):
	"""
	This class implements triggers to select text within pair characters.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: An BracketSelectionTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_triggers()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__select_bracket_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = self.__signal_id_1 = None
		from gtksourceview import source_iter_find_matching_bracket
		self.__match = source_iter_find_matching_bracket
		return

########################################################################
#
#							Public Method
#
########################################################################

	def destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.
		"""
		self.__destroy()
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __create_triggers(self):
		"""
		Create the trigger.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.
		"""
		from SCRIBES.Trigger import Trigger
		self.__trigger = Trigger("select_text_within_characters", "alt - b")
		self.__editor.add_trigger(self.__trigger)
		return

	def __select_text_within_pair_characters(self):
		"""
		Select text within pair characters if possible.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.

		@return: True if the operation succeeded.
		@rtype: A Boolean object.
		"""
		open_pair_characters = ("(", "[", "{", "<")
		from SCRIBES.cursor import get_cursor_iterator
		cursor_iterator = get_cursor_iterator(self.__editor.textbuffer)
		transition_iterator = cursor_iterator.copy()
		from operator import truth, contains, ge
		while True:
			if truth(transition_iterator.is_start()): break
			transition_iterator.backward_char()
			if contains(open_pair_characters, transition_iterator.get_char()):
				begin = transition_iterator.copy()
				if truth(self.__match(begin)):
					if ge(begin.compare(cursor_iterator), 0):
						transition_iterator.forward_char()
						self.__editor.textbuffer.select_range(transition_iterator, begin)
						return True
		return False

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: An BracketSelectionTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__signal_id_1, self.__trigger)
		delete_attributes(self)
		del self
		self = None
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __select_bracket_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BracketSelectionTrigger instance.
		@type self: A BracketSelectionTrigger object.

		@param trigger: A trigger for the pair character selection function.
		@type trigger: A Trigger object.
		"""
		if self.__select_text_within_pair_characters():
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "succeed")
		else:
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "fail")
		return
