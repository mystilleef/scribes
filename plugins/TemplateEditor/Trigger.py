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
This module documents a class that creates a trigger that shows the
template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class TemplateEditorTrigger(GObject):
	"""
	This class creates an object that shows the text editor's template
	editor.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the TemplateEditorTrigger instance.
		@type self: An TemplateEditorTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_editor)
		self.__signal_id_2 = self.connect_after("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the TemplateEditorTrigger instance.
		@type self: A TemplateEditorTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None
		self.__trigger = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		from MenuItem import MenuItem
		MenuItem(self, editor)
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the TemplateEditorTrigger instance.
		@type self: A TemplateEditorTrigger object.
		"""
		# Trigger to show the about dialog.
		self.__trigger = self.__editor.create_trigger("show_template_editor", "alt - F12")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_editor(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the TemplateEditorTrigger instance.
		@type self: A TemplateEditorTrigger object.

		@param trigger: An object to show template editor
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.show()
		except AttributeError:
			from Manager import TemplateManager
			self.__manager = TemplateManager(self, self.__editor)
			self.__manager.show()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the TemplateEditorTrigger instance.
		@type self: An TemplateEditorTrigger object.

		@param trigger: Reference to the TemplateEditorTrigger instance.
		@type trigger: An TemplateEditorTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		del self
		self = None
		return
