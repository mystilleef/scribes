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
This module documents a class that creates an error dialog for the text
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import MessageDialog

class ScribesErrorDialog(MessageDialog):
	"""
	This class creates an object that shows a dialog with an error
	message. The class defines the default properties and behavior of
	the dialog. The class exposes one public API method:

		show_message(message, title_message=None, parent_window=None)

	To show a dialog with an error message, use the following API:

		editor.error_dialog.show_message(message)

	where editor is an Editor object.
	"""

	def show_message(self, error_message, title_message=None, parent_window=None):
		"""
		Show an error message on the dialog.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.

		@param error_message: A message describing an error.
		@type error_message: A String object.

		@param title_message: A title for the error message.
		@type title_message: A String object.

		@param parent_window: The parent window for the dialog.
		@type parent_window: A gtk.Window object.
		"""
		if parent_window:
			self.set_transient_for(parent_window)
			if parent_window.get_property("name") in ["EditorWindow"]:
				self.__use_signals = True
		if title_message:
			self.set_property("secondary-text", error_message)
			self.set_property("text", title_message)
		else:
			self.set_property("text", error_message)
		self.__show_dialog()
		return

	def __init__(self, editor):
		"""
		Initialize the dialog.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gtk import MESSAGE_ERROR
		MessageDialog.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = self.connect("response", self.__response_cb)
		self.__signal_id_2 = self.connect("close", self.__delete_event_cb)
		self.__signal_id_3 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_4 = self.__editor.connect("close-document-no-save", self.__close_document_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog's data attributes.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__use_signals = False
		self.__editor = editor
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__registration_id = editor.register_object()
		return

	def __set_properties(self):
		"""
		Set the error dialog's properties

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.
		"""
		self.set_property("name", "scribes error dialog")
		from gtk import STOCK_CLOSE, RESPONSE_CLOSE
		self.add_button(STOCK_CLOSE, RESPONSE_CLOSE)
		from gtk import MESSAGE_ERROR
		self.set_property("message-type", MESSAGE_ERROR)
		from internationalization import msg0133
		self.set_property("title", msg0133)
		self.set_property("role", "error_message_dialog")
		self.set_property("icon-name", "stock_dialog-error")
		self.set_property("skip-pager-hint", True)
		self.set_property("skip-taskbar-hint", True)
		self.set_property("urgency-hint", False)
		self.set_property("modal", True)
		from gtk import WIN_POS_CENTER_ON_PARENT
		self.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		self.set_property("resizable", True)
		return

	def __show_dialog(self):
		"""
		Show the dialog.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
		"""
		if self.__use_signals: self.__editor.emit("show-dialog", self)
		self.run()
		return

	def __hide_dialog(self):
		"""
		Hide the dialog.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.
		"""
		if self.__use_signals: self.__editor.emit("hide-dialog", self)
		self.hide()
		self.__use_signals = False
		return

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		# Unregister object so that editor can quit.
		self.destroy()
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return

################################################################################
#
#							Dialog  Callbacks
#
################################################################################

	def __response_cb(self, *args):
		"""
		Handles callback when keys on the keyboard are pressed.

		This function watches for the Escape key event. When the Escape key
		event is detected, this function closes text editor's about dialog.

		@param dialog: The text editor's about dialog.
		@type dialog: A ScribesDialog object.

		@param event: An event generated by pressing the keyboard.
		@type event: A gtk.Event object

		@return: If false, propagate the generated event. Otherwise, block the
				event.
		@rtype: A boolean value.
		"""
		self.__hide_dialog()
		return False

	def __delete_event_cb(self, *args):
		"""
		Handles callback when keys on the keyboard are pressed.

		This function watches for the Escape key event. When the Escape key
		event is detected, this function closes text editor's about dialog.

		@param dialog: The text editor's about dialog.
		@type dialog: A ScribesDialog object.

		@param event: An event generated by pressing the keyboard.
		@type event: A gtk.Event object

		@return: If false, propagate the generated event. Otherwise, block the
				event.
		@rtype: A boolean value.

		"""
		self.__hide_dialog()
		return False

	def __close_document_cb(self, editor):
		self.__destroy()
		return False

