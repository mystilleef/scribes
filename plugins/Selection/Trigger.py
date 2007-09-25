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
This module documents a class that creates triggers to perform selection
operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class SelectionTrigger(GObject):
	"""
	This class creates an object, a trigger, that allows users to
	perform selection operations.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the SelectionTrigger instance.
		@type self: A SelectionTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__select_word_trigger.connect("activate", self.__select_word_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)
		self.__signal_id_3 = self.__select_sentence_trigger.connect("activate", self.__select_sentence_cb)
		self.__signal_id_4 = self.__select_line_trigger.connect("activate", self.__select_line_cb)
		self.__signal_id_6 = self.__editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the SelectionTrigger instance.
		@type self: A SelectionTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__select_word_trigger = None
		self.__select_sentence_trigger = None
		self.__select_line_trigger = None
		self.__select_paragraph_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_6 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the SelectionTrigger instance.
		@type self: A SelectionTrigger object.
		"""
		# Trigger to select a word.
		from SCRIBES.Trigger import Trigger
		self.__select_word_trigger = Trigger("select_word", "alt - w")
		self.__editor.add_trigger(self.__select_word_trigger)

		# Trigger to select a sentence.
		self.__select_sentence_trigger = Trigger("select_sentence", "alt - s")
		self.__editor.triggermanager.add_trigger(self.__select_sentence_trigger)

		# Trigger to select a line.
		self.__select_line_trigger = Trigger("select_line", "alt - l")
		self.__editor.triggermanager.add_trigger(self.__select_line_trigger)
		return

	def __select_word_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: A SelectionTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		# Prevent this action from occurring when the text editor is in
		# readonly mode.
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from SCRIBES.cursor import get_cursor_iterator
		iterator = get_cursor_iterator(self.__editor.textbuffer)
		from word import select_word
		result = select_word(self.__editor.textbuffer, iterator)
		if result:
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "succeed")
		else:
			from i18n import msg0003
			self.__editor.feedback.update_status_message(msg0003, "fail")
		return

	def __select_sentence_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: A SelectionTrigger object.

		@param trigger: An object that selects a sentence.
		@type trigger: A Trigger object.
		"""
		# Prevent this action from occurring when the text editor is in
		# readonly mode.
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot be
			# performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from sentence import select_sentence
		result = select_sentence(self.__editor.textbuffer)
		if result:
			from i18n import msg0004
			self.__editor.feedback.update_status_message(msg0004, "succeed")
		else:
			from i18n import msg0005
			self.__editor.feedback.update_status_message(msg0005, "fail")
		return

	def __select_line_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: A SelectionTrigger object.

		@param trigger: An object that selects a line.
		@type trigger: A Trigger object.
		"""
		# Prevent this action from occurring when the text editor is in readonly
		# mode.
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot be
			# performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from SCRIBES.cursor import get_cursor_line
		cursor_line = get_cursor_line(self.__editor.textbuffer)
		from lines import select_line
		result = select_line(self.__editor.textbuffer)
		if result:
			from i18n import msg0007
			message = msg0007 % (cursor_line + 1)
			self.__editor.feedback.update_status_message(message, "succeed")
		else:
			from i18n import msg0006
			message = msg0006 % (cursor_line + 1)
			self.__editor.feedback.update_status_message(message, "fail")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: An SelectionTrigger object.

		@param trigger: Reference to the SelectionTrigger instance.
		@type trigger: A SelectionTrigger object.
		"""
		self.__editor.triggermanager.remove_trigger(self.__select_word_trigger)
		self.__editor.triggermanager.remove_trigger(self.__select_sentence_trigger)
		self.__editor.triggermanager.remove_trigger(self.__select_line_trigger)
		if self.__signal_id_1 and self.__select_word_trigger.handler_is_connected(self.__signal_id_1):
			self.__select_word_trigger.disconnect(self.__signal_id_1)
		if self.__signal_id_2 and self.handler_is_connected(self.__signal_id_2):
			self.disconnect(self.__signal_id_2)
		if self.__signal_id_3 and self.__select_sentence_trigger.handler_is_connected(self.__signal_id_3):
			self.__select_sentence_trigger.disconnect(self.__signal_id_3)
		if self.__signal_id_4 and self.__select_line_trigger.handler_is_connected(self.__signal_id_4):
			self.__select_line_trigger.disconnect(self.__signal_id_4)
		if self.__signal_id_6 and self.__editor.textview.handler_is_connected(self.__signal_id_6):
			self.__editor.textview.disconnect(self.__signal_id_6)
		del self.__editor, self.__select_word_trigger
		del self.__select_sentence_trigger, self.__select_line_trigger
		del self.__signal_id_2, self.__signal_id_1, self.__signal_id_3
		del self.__signal_id_4, self.__signal_id_6
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: An SelectionTrigger object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from PopupMenuItem import SelectionPopupMenuItem
		menu.prepend(SelectionPopupMenuItem(self.__editor))
		menu.show_all()
		return False
