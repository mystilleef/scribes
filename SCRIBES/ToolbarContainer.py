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
This module exposes a class that creates the toolbar container for the text
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import HBox

class ScribesToolbarContainer(HBox):
	"""
	This class creates the toolbar container object for the text editor. The
	toolbar container houses the text editor's toolbar object.
	"""

	def __init__(self, editor):
		"""
		Initialize instance of this class.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		HBox.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_4 = editor.connect("hide-bar", self.__hide_bar_cb)
		self.__signal_id_5 = editor.connect("show-dialog", self.__show_dialog_cb)
		self.__signal_id_6 = editor.connect("hide-dialog", self.__hide_dialog_cb)
		self.__signal_id_7 = editor.connect("enable-fullscreen", self.__enable_fullscreen_cb)
		self.__signal_id_8 = editor.connect("disable-fullscreen", self.__disable_fullscreen_cb)
		editor.response()

	def __init_attributes(self, editor):
		"""
		Initialize the text editor's toolbar container and set its default
		state and properties.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__registration_id = editor.register_object()
		# Initialize the fullscreen button.
		self.__fsbutton = None
		self.__timer = None
		self.__handler_id = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = None
		return

	def __set_properties(self):
		"""
		Set the toolbar container's properties.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.
		"""
		self.set_property("name", "ScribesToolbarContainer")
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
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__handler_id, self.__editor.window)
		if self.__fsbutton: self.__fsbutton.destroy()
		self.destroy()
		# Unregister object so that editor can quit.
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return

	def __close_document_cb(self, editor):
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

	def __show_bar_cb(self, editor, bar):
		self.set_property("sensitive", False)
		return

	def __hide_bar_cb(self, editor, bar):
		self.set_property("sensitive", True)
		return

	def __enable_fullscreen_cb(self, editor):
		"""
		Handles callback when the "enable-fullscreen" signal is emitted.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import timeout_add
		self.__timer = timeout_add(5000, self.__hide_toolbarcontainer)
		try:
			self.__fsbutton.show_all()
			self.pack_end(self.__fsbutton, False, False, 0)
		except:
			from fsbutton import ScribesFullscreenButton
			self.__fsbutton = ScribesFullscreenButton(self.__editor)
			self.__fsbutton.show_all()
			self.pack_end(self.__fsbutton, False, False, 0)
		self.queue_resize()
		self.resize_children()
		self.__handler_id = editor.window.connect("motion-notify-event",
								self.__motion_notify_event_cb)
		return

	def __disable_fullscreen_cb(self, editor):
		"""
		Handles callback when the "disable-fullscreen" signal is emitted.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.window.disconnect(self.__handler_id)
		from gobject import source_remove
		source_remove(self.__timer)
		self.__fsbutton.hide_all()
		self.remove(self.__fsbutton)
		self.show_all()
		self.queue_resize()
		self.resize_children()
		self.__handler_id = self.__timer = None
		return

	def __motion_notify_event_cb(self, window, event):
		"""
		Handles callback when the "motion-notify-event" signal is emitted.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@param window: The window for the text editor.
		@type window: A ScribesWindow object.

		@param event: An event that occurs when the mouse moves.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		window.window.get_pointer()
		self.show_all()
		from gobject import source_remove
		source_remove(self.__timer)
		from gobject import timeout_add
		self.__timer = timeout_add(5000, self.__hide_toolbarcontainer)
		return False

	def __hide_toolbarcontainer(self):
		"""
		Hide the toolbar container.

		@param self: Reference to the ScribesToolbarContainer instance.
		@type self: A ScribesToolbarContainer object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		if self.__editor.window.is_fullscreen: self.hide_all()
		return False
