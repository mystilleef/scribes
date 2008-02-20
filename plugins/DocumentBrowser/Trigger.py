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
This module documents a class that creates a trigger to show the bookmark
browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class DocumentBrowserTrigger(GObject):
	"""
	This class creates an object, a trigger, that allows users to show
	the document browser.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the DocumentBrowserTrigger instance.
		@type self: A DocumentBrowserTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_document_browser_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the DocumentBrowserTrigger instance.
		@type self: A DocumentBrowserTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = None
		self.__trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the DocumentBrowserTrigger instance.
		@type self: A DocumentBrowserTrigger object.
		"""
		# Trigger to show a document browser.
		self.__trigger = self.__editor.create_trigger("show_document_browser", "F9")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_document_browser_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the DocumentBrowserTrigger instance.
		@type self: A DocumentBrowserTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.show_browser()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the DocumentBrowserTrigger instance.
		@type self: An DocumentBrowserTrigger object.

		@param trigger: Reference to the DocumentBrowserTrigger instance.
		@type trigger: A DocumentBrowserTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		if self.__manager: self.__manager.emit("destroy")
		del self
		self = None
		return
