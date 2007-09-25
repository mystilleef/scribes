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
This module exposes a class that creates the main container for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import VBox

class ScribesMainContainer(VBox):
	"""
	This class creates the main container object for the text editor. The main
	container is the topmost container object. The main container is embedded
	within the text editor's window.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the ScribesMainContainer instance.
		@type self: A ScribesMainContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		VBox.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.resize_children()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_4 = editor.connect("hide-bar", self.__hide_bar_cb)
		editor.response()

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the ScribesMainContainer instance.
		@type self: A ScribesMainContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__bar_is_visible = False
		self.__registration_id = editor.register_termination_id()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __set_properties(self):
		"""
		Set object properties.

		@param self: Reference to the ScribesMainContainer instance.
		@type self: A ScribesMainContainer object.
		"""
		from gtk import RESIZE_PARENT
		self.set_property("resize-mode", RESIZE_PARENT)
		self.set_property("parent", self.__editor.window)
		self.set_property("name", "scribesmaincontainer")
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		# Disconnect signals.
		from utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__editor)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self.__editor)
		disconnect_signal(self.__signal_id_4, self.__editor)
		#self.destroy()
		# Unregister object so that editor can quit.
		self.__editor.unregister_termination_id(self.__registration_id)
		delete_attributes(self)
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

	def __show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesMainContainer instance.
		@type self: A ScribesMainContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's bar.
		@type bar: A ScribesBar object.
		"""
		if self.__bar_is_visible:
			return
		self.pack_start(bar, False, False, 0)
		self.reorder_child(bar, 2)
		bar.show_all()
		self.__bar_is_visible = True
		return

	def __hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesMainContainer instance.
		@type self: A ScribesMainContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's bar.
		@type bar: A ScribesBar object.
		"""
		bar.hide_all()
		self.__bar_is_visible = False
		self.remove(bar)
		return
