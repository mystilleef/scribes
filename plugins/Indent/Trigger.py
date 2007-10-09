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
This module documents a class that creates a trigger that indents lines.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class IndentTrigger(GObject):
	"""
	This class creates an object, a trigger, that indents or unindents
	lines in the text editor's buffer.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the IndentTrigger instance.
		@type self: A IndentTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__indent_cb)
		self.__signal_id_3 = self.__unindent_trigger.connect("activate", self.__unindent_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)
		self.__signal_id_4 = self.__editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the IndentTrigger instance.
		@type self: A IndentTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__unindent_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the IndentTrigger instance.
		@type self: A IndentTrigger object.
		"""
		# Trigger to indent lines.
		self.__trigger = self.__editor.create_trigger("indent_line", "ctrl - t")
		self.__editor.add_trigger(self.__trigger)

		# Trigger to unindent lines.
		self.__unindent_trigger = self.__editor.create_trigger("unindent_line", "ctrl - T")
		self.__editor.add_trigger(self.__unindent_trigger)
		return

	def __indent_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the IndentTrigger instance.
		@type self: A IndentTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Prevent indentation operations when the text editor is in
			# readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from i18n import msg0002
		status_id = self.__editor.feedback.set_modal_message(msg0002, "run")
		self.__editor.show_busy_cursor()
		from indent import indent
		lines_indented = indent(self.__editor.textview)
		self.__editor.show_normal_cursor()
		self.__editor.feedback.unset_modal_message(status_id, False)
		if len(lines_indented) > 1:
			from i18n import msg0003
			self.__editor.feedback.update_status_message(msg0003, "succeed")
		else:
			from i18n import msg0004
			value = lines_indented[0] + 1
			message = msg0004 % (value)
			self.__editor.feedback.update_status_message(message, "succeed")
		return

	def __unindent_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the UnindentTrigger instance.
		@type self: A UnindentTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Prevent save operations when the text editor is in readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		from i18n import msg0002
		status_id = self.__editor.feedback.set_modal_message(msg0002, "run")
		self.__editor.show_busy_cursor()
		from unindent import unindent
		lines_unindented = unindent(self.__editor.textview)
		self.__editor.show_normal_cursor()
		self.__editor.feedback.unset_modal_message(status_id, False)
		if not lines_unindented:
			from i18n import msg0005
			self.__editor.feedback.update_status_message(msg0005, "fail")
		elif len(lines_unindented) > 1:
			from i18n import msg0006
			self.__editor.feedback.update_status_message(msg0006, "succeed")
		else:
			from i18n import msg0007
			value = lines_unindented[0] + 1
			message = msg0007 % (value)
			self.__editor.feedback.update_status_message(message, "succeed")
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the IndentTrigger instance.
		@type self: An IndentTrigger object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from PopupMenuItem import IndentPopupMenuItem
		menu.prepend(IndentPopupMenuItem(self.__editor))
		menu.show_all()
		return False

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the IndentTrigger instance.
		@type self: An IndentTrigger object.

		@param trigger: Reference to the IndentTrigger instance.
		@type trigger: A IndentTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.remove_trigger(self.__unindent_trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__unindent_trigger)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor.textview)
		del self
		self = None
		return
