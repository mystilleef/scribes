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
This module exposes a class that creates the container for the editor's
statusbar area.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import HBox

class ScribesStatusContainer(HBox):
	"""
	This class creates the statusbar container object for the text editor. The
	object houses the text editor's statusbar.
	"""

	def __init__(self, editor):
		"""
		Initialize the text editor's statusbar container and set its default
		state and properties.

		@param self: Reference to the ScribesStatusContainer instance.
		@type self: A ScribesStatusContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		HBox.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.resize_children()
		self.__set_visibility()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = editor.connect("enable-fullscreen", self.__enable_fullscreen_cb)
		self.__signal_id_4 = editor.connect("disable-fullscreen", self.__disable_fullscreen_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__hide_status_area_cb)

	def __get_visibility(self):
		return self.__is_visible

	is_visible = property(__get_visibility, doc="Whether or not the status area is visible")

	def __init_attributes(self, editor):
		"""
		Initialize the container's attributes.

		@param self: Reference to the ScribesStatusContainer instance.
		@type self: A ScribesStatusContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__is_visible = False
		self.__registration_id = editor.register_object()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "MinimalMode.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __set_properties(self):
		"""
		Set the container's properties.

		@param self: Reference to the ScribesStatusContainer instance.
		@type self: A ScribesStatusContainer object.
		"""
		self.set_no_show_all(True)
#		from gtk import RESIZE_PARENT
#		self.set_property("resize-mode", RESIZE_PARENT)
		self.set_property("name", "scribesstatuscontainer")
		return

	def __set_visibility(self):
		"""
		Determine whether to show the status area.

		@param self: Reference to the Toolbar instance.
		@type self: A Toolbar object.
		"""
		from MinimalModeMetadata import get_value
		hide_status_area = get_value()
		if hide_status_area:
			self.set_no_show_all(True)
			self.__is_visible = False
			self.hide()
		else:
			self.set_no_show_all(False)
			self.__is_visible = True
			self.show_all()
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
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
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

	def __enable_fullscreen_cb(self, editor):
		"""
		Handles callback when the "enable-fullscreen" signal is emitted.

		@param self: Reference to the ScribesStatusContainer instance.
		@type self: A ScribesStatusContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.hide_all()
		return

	def __disable_fullscreen_cb(self, editor):
		"""
		Handles callback when the "disable-fullscreen" signal is emitted.

		@param self: Reference to the ScribesStatusContainer instance.
		@type self: A ScribesStatusContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.show_all()
		return

	def __hide_status_area_cb(self, *args):
		self.__set_visibility()
		return
