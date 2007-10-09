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
This module documents a class that creates a trigger perform line
operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class LinesTrigger(GObject):
	"""
	This class creates an object, a trigger, that performs line
	operations.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__delete_line_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)
		self.__signal_id_3 = self.__trigger_1.connect("activate", self.__join_line_cb)
		self.__signal_id_4 = self.__trigger_2.connect("activate", self.__free_line_above_cb)
		self.__signal_id_5 = self.__trigger_3.connect("activate", self.__free_line_below_cb)
		self.__signal_id_6 = self.__trigger_4.connect("activate", self.__cursor_to_end_cb)
		self.__signal_id_7 = self.__trigger_5.connect("activate", self.__cursor_to_start_cb)
		self.__signal_id_8 = self.__editor.textview.connect_after("populate-popup", self.__popup_cb)
		self.__signal_id_9 = self.__trigger_6.connect("activate", self.__duplicate_line_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__trigger_1 = None
		self.__trigger_2 = None
		self.__trigger_3 = None
		self.__trigger_4 = None
		self.__trigger_5 = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__signal_id_6 = None
		self.__signal_id_7 = None
		self.__signal_id_8 = None
		self.__signal_id_9 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.
		"""
		# Trigger to delete a line.
		self.__trigger = self.__editor.create_trigger("delete_line", "alt - d")
		self.__editor.add_trigger(self.__trigger)

		# Trigger to join lines.
		self.__trigger_1 = self.__editor.create_trigger("join_line", "alt - j")
		self.__editor.add_trigger(self.__trigger_1)

		# Trigger to free the current line.
		self.__trigger_2 = self.__editor.create_trigger("free_line_above", "alt - O")
		self.__editor.add_trigger(self.__trigger_2)

		# Trigger to free the next line.
		self.__trigger_3 = self.__editor.create_trigger("free_line_below", "alt - o")
		self.__editor.add_trigger(self.__trigger_3)

		# Trigger to delete from cursor to line end.
		self.__trigger_4 = self.__editor.create_trigger("delete_cursor_to_end", "alt - End")
		self.__editor.add_trigger(self.__trigger_4)

		# Trigger to delete from cursor to line start.
		self.__trigger_5 = self.__editor.create_trigger("delete_cursor_to_begin", "alt - Home")
		self.__editor.add_trigger(self.__trigger_5)

		# Trigger to duplicate line or selected lines.
		self.__trigger_6 = self.__editor.create_trigger("duplicate_line", "ctrl - D")
		self.__editor.add_trigger(self.__trigger_6)
		return

	def __delete_line_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param trigger: An object that deletes a line.
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
		cursor_line = self.__editor.get_cursor_line()
		from lines import delete_line
		delete_line(self.__editor.textbuffer)
		from i18n import msg0002
		message = msg0002 % (cursor_line + 1)
		self.__editor.feedback.update_status_message(message, "succeed")
		return

	def __duplicate_line_cb(self, *args):
		# Prevent this action from occurring when the text editor is in
		# readonly mode.
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from lines import duplicate_line
		duplicate_line(self.__editor.textbuffer)
		self.__editor.move_view_to_cursor()
		from i18n import msg0017
		self.__editor.feedback.update_status_message(msg0017, "yes")
		return

	def __join_line_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param trigger: An object that joins lines.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			editor.feedback.update_status_message(msg0001, "fail")
			return
		cursor_line = self.__editor.get_cursor_line()
		from lines import join_line
		result = join_line(self.__editor.textbuffer)
		if result:
			from i18n import msg0003
			message = msg0003 % (cursor_line+1, cursor_line+2)
			self.__editor.feedback.update_status_message(message, "succeed")
		else:
			from i18n import msg0004
			self.__editor.feedback.update_status_message(msg0004, "fail")
		return

	def __free_line_above_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param trigger: An object that frees the current line.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from lines import free_line_above
		line_number = free_line_above(self.__editor.textbuffer)
		self.__editor.move_view_to_cursor()
		from i18n import msg0005
		message = msg0005 % (line_number+1)
		self.__editor.feedback.update_status_message(message, "succeed")
		return

	def __free_line_below_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param trigger: An object that frees the next line.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from lines import free_line_below
		line_number = free_line_below(self.__editor.textbuffer)
		self.__editor.move_view_to_cursor()
		from i18n import msg0005
		message = msg0005 % (line_number+1)
		self.__editor.feedback.update_status_message(message, "succeed")
		return

	def __cursor_to_end_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param trigger: An object that deletes from cursor to end of line.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		cursor_line = self.__editor.get_cursor_line()
		from lines import delete_cursor_to_line_end
		result = delete_cursor_to_line_end(self.__editor.textbuffer)
		if result:
			from i18n import msg0006
			message = msg0006 % (cursor_line+1)
			self.__editor.feedback.update_status_message(message, "succeed")
		else:
			from i18n import msg0007
			self.__editor.feedback.update_status_message(msg0007, "fail")
		return

	def __cursor_to_start_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: A LinesTrigger object.

		@param trigger: An object that deletes from cursor to start of line.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Feedback to the status bar indicating the operation cannot
			# be performed.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		cursor_line = self.__editor.get_cursor_line()
		from lines import delete_cursor_to_line_begin
		result = delete_cursor_to_line_begin(self.__editor.textbuffer)
		if result:
			from i18n import msg0008
			message = msg0008 % (cursor_line+1)
			self.__editor.feedback.update_status_message(message, "succeed")
		else:
			from i18n import msg0009
			self.__editor.feedback.update_status_message(msg0009, "fail")
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: An LinesTrigger object.

		@param trigger: Reference to the LinesTrigger instance.
		@type trigger: A LinesTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.remove_trigger(self.__trigger_1)
		self.__editor.remove_trigger(self.__trigger_2)
		self.__editor.remove_trigger(self.__trigger_3)
		self.__editor.remove_trigger(self.__trigger_4)
		self.__editor.remove_trigger(self.__trigger_5)
		self.__editor.remove_trigger(self.__trigger_6)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__trigger_1)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__trigger_2)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__trigger_3)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__trigger_4)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__trigger_5)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__trigger_6)
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the LinesTrigger instance.
		@type self: An LinesTrigger object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from PopupMenuItem import LinesPopupMenuItem
		menu.prepend(LinesPopupMenuItem(self.__editor))
		menu.show_all()
		return False
