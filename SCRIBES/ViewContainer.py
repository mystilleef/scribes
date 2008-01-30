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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class that creates the container for the editor's view.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import HBox

class ScribesViewContainer(HBox):
	"""
	This class creates the view container object for the text editor. The object
	houses the text editor's viewing area.
	"""

	def __init__(self, editor):
		"""
		Initialize instance of this class.

		@param self: Reference to the ScribesViewContainer instance.
		@type self: A ScribesViewContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.response()
		HBox.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = editor.connect("show-dialog", self.__show_dialog_cb)
		self.__signal_id_4 = editor.connect("hide-dialog", self.__hide_dialog_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the container's attributes.

		@param self: Reference to the ScribesViewContainer instance.
		@type self: A ScribesViewContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__registration_id = editor.register_object()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __set_properties(self):
		"""
		Set the container's properties.

		@param self: Reference to the ScribesViewContainer instance.
		@type self: A ScribesViewContainer object.
		"""
		self.set_property("name", "scribesviewcontainer")
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		# Unregister object so that editor can quit.
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__destroy()
		return

	def __show_dialog_cb(self, editor, dialog):
		"""
		Handles callback when the "show-dialog" signal is emitted.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __hide_dialog_cb(self, editor, dialog):
		"""
		Handles callback when the "hide-dialog" signal is emitted.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return
