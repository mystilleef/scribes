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
This module documents a class that creates a menu for the text editor's
preference toolbar button.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Menu

class PreferenceMenu(Menu):
	"""
	This class creates a menu for the text editor's preference toolbar
	button.
	"""

	def __init__(self, editor):
		"""
		Initialize the menu.

		@param self: Reference to the PreferenceMenu instance.
		@type self: A PreferenceMenu object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Menu.__init__(self)
		self.__init_attributes(editor)
		self.show_all()
		self.__signal_id_1 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = self.__editor.connect("close-document-no-save", self.__close_document_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the menu's attributes.

		@param self: Reference to the PreferenceMenu instance.
		@type self: A PreferenceMenu object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__registration_id = editor.register_object()
		return

	def __destroy(self):
		"""
		Destroy object.
		
		@param self: Reference to the PreferenceMenu.
		@type self: A PreferenceMenu object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		# Unregister object so that editor can quit.
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return
		
	def __close_document_cb(self, editor):
		self.__destroy()
		return
