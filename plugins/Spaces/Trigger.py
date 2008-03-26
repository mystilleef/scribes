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
This module documents a class that creates a trigger that toggles spell
checking.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class SpacesTrigger(GObject):
	"""
	This class creates an object, a trigger, that toggles spell
	checking.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the SpacesTrigger instance.
		@type self: A SpacesTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__spaces_trigger.connect("activate", self.__spaces_to_tabs_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)
		self.__signal_id_3 = self.__tabs_trigger.connect("activate", self.__tabs_to_spaces_cb)
		self.__signal_id_4 = self.__remove_trigger.connect("activate", self.__remove_trailing_spaces_cb)
		self.__signal_id_5 = self.__editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the SpacesTrigger instance.
		@type self: A SpacesTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__spaces_trigger = None
		self.__tabs_trigger = None
		self.__remove_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the SpacesTrigger instance.
		@type self: A SpacesTrigger object.
		"""
		# Trigger to convert spaces to tabs
		self.__spaces_trigger = self.__editor.create_trigger("spaces_to_tabs", "alt - t")
		self.__editor.add_trigger(self.__spaces_trigger)

		# Trigger to convert tabs to spaces.
		self.__tabs_trigger = self.__editor.create_trigger("tabs_to_spaces", "alt - T")
		self.__editor.add_trigger(self.__tabs_trigger)

		# Trigger to remove trailing spaces.
		self.__remove_trigger = self.__editor.create_trigger("removes_trailing_space", "alt - r")
		self.__editor.add_trigger(self.__remove_trigger)
		return

	def __spaces_to_tabs_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SpacesTrigger instance.
		@type self: A SpacesTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		if self.__editor.is_readonly:
			# Prevent save operations when the text editor is in readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		self.__editor.block_response()
		from i18n import msg0002
		status_id = self.__editor.feedback.set_modal_message(msg0002, "run")
		self.__editor.show_busy_cursor()
		from spaces import convert_spaces_to_tabs
		converted_lines = convert_spaces_to_tabs(self.__editor.textview)
		self.__editor.show_normal_cursor()
		self.__editor.feedback.unset_modal_message(status_id, False)
		if not converted_lines:
			from i18n import msg0003
			self.__editor.feedback.update_status_message(msg0003, "fail")
		else:
			from i18n import msg0004
			self.__editor.feedback.update_status_message(msg0004, "succeed")
		self.__editor.unblock_response()
		return

	def __tabs_to_spaces_cb(self, trigger):
		if self.__editor.is_readonly:
			# Prevent save operations when the text editor is in readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		self.__editor.block_response()
		from i18n import msg0005
		status_id = self.__editor.feedback.set_modal_message(msg0005, "run")
		self.__editor.show_busy_cursor()
#		from SCRIBES.cursor import show_busy_textview_cursor
#		show_busy_textview_cursor(self.__editor.textview)
		from spaces import convert_tabs_to_spaces
		converted_lines = convert_tabs_to_spaces(self.__editor.textview)
		self.__editor.show_normal_cursor()
		self.__editor.feedback.unset_modal_message(status_id, False)
		if not converted_lines:
			from i18n import msg0007
			self.__editor.feedback.update_status_message(msg0007, "fail")
		else:
			from i18n import msg0006
			self.__editor.feedback.update_status_message(msg0006, "succeed")
		self.__editor.unblock_response()
		return

	def __remove_trailing_spaces_cb(self, trigger):
		if self.__editor.is_readonly:
			# Prevent save operations when the text editor is in
			# readonly mode.
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		self.__editor.block_response()
		from i18n import msg0008
		status_id = self.__editor.feedback.set_modal_message(msg0008, "run")
		self.__editor.show_busy_cursor()
		from spaces import remove_trailing_spaces
		affected_lines = remove_trailing_spaces(self.__editor.textview)
		self.__editor.show_normal_cursor()
		self.__editor.feedback.unset_modal_message(status_id, False)
		if not affected_lines:
			from i18n import msg0009
			self.__editor.feedback.update_status_message(msg0009, "fail")
		else:
			from i18n import msg0010
			self.__editor.feedback.update_status_message(msg0010, "succeed")
		self.__editor.unblock_response()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SpacesTrigger instance.
		@type self: An SpacesTrigger object.

		@param trigger: Reference to the SpacesTrigger instance.
		@type trigger: A SpacesTrigger object.
		"""
		self.__editor.triggermanager.remove_trigger(self.__spaces_trigger)
		self.__editor.triggermanager.remove_trigger(self.__tabs_trigger)
		self.__editor.triggermanager.remove_trigger(self.__remove_trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__spaces_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__tabs_trigger)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__remove_trigger)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor.textview)
		del self
		self = None
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
		from PopupMenuItem import SpacesPopupMenuItem
		menu.prepend(SpacesPopupMenuItem(self.__editor))
		menu.show_all()
		return False
