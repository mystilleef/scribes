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
Error dialogs for text editor instances.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import MessageDialog

class ScribesErrorDialog(MessageDialog):
	"""
	This class creates an error dialog for text editor instances. It inherits
	from gtk.MessageDialog. See the PyGTK, or GTK+, manual for more information
	on the gtk.MessageDialog class.
	"""

	def __init__(self, editor, filename, message):
		"""
		Initialize and show an error dialog containing an error message.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.

		@param window: The transient window for the error dialog.
		@type window: A gtk.Window object.

		@param filename: The name of the filename for which an error has occured.
		@type filename: A String object.

		@param message: The error message to display to the user.
		@type message: A String object.
		"""
		MessageDialog.__init__(self, message_format="File: " + filename)
		self.__init_attributes(message, editor)
		self.__set_properties()
		self.connect("key-press-event", self.__key_press_event_cb)
		self.connect("delete-event", self.__delete_event_cb)
		self.show_dialog()

	def __init_attributes(self, message, editor):
		"""
		Initialize the error dialog's attributes.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: An ScribesErrorDialog object.

		@param window: The transient window for the error dialog.
		@type window: A gtk.Window object.

		@param filename: The name of the filename for which an error has occured.
		@type filename: A String object.

		@param message: The error message to display to the user.
		@type message: A String object.
		"""
		self.secondary_message = message
		self.editor = editor
		return

	def __set_properties(self):
		"""
		Set the error dialog's properties

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.
		"""
		from gtk import STOCK_CLOSE, RESPONSE_CLOSE
		self.add_button(STOCK_CLOSE, RESPONSE_CLOSE)
		from gtk import MESSAGE_ERROR
		self.set_property("message-type", MESSAGE_ERROR)
		self.format_secondary_markup(self.secondary_message)
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
		try:
			self.set_transient_for(self.editor.window)
		except:
			pass
		return

	def show_dialog(self):
		"""
		Show the dialog.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
		"""
		self.editor.emit("show-dialog", self)
		self.show_all()
		self.run()
		self.hide_dialog()
		return

	def hide_dialog(self):
		"""
		Hide the dialog.

		@param self: Reference to the ScribesErrorDialog instance.
		@type self: A ScribesErrorDialog object.
		"""
		self.editor.emit("hide-dialog", self)
		self.hide()
		from gobject import timeout_add
		# Feedback to the text editor's statusbar indication the dialog window
		# has just been closed.
		try:
			from internationalization import msg0187
			timeout_add(10, self.editor.feedback.update_status_message, msg0187,
						"info", 1)
		except:
			pass
		self = None
		del self
		return

################################################################################
#
#							Dialog  Callbacks
#
################################################################################

	def __key_press_event_cb(self, dialog, event):
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
		from gtk import keysyms
		# Close the text editor's about dialog when the escape key is pressed.
		if event.keyval == keysyms.Escape:
			from gtk import RESPONSE_CLOSE
			dialog.response(RESPONSE_CLOSE)
		return False

	def __delete_event_cb(self, dialog, event):
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
		from gtk import RESPONSE_CLOSE
		dialog.response(RESPONSE_CLOSE)
		return True
