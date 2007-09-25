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
This module exposes a base class for all dialogs used by the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Dialog

class ScribesDialog(Dialog):
	"""
	This class defines the basic properties and behavior for all dialogs of the
	text editor. Its primary objective is for inheritance. It inherits from the
	gtk.Dialog. See the GTK+ manual for the properties gtk.Dialog exposes.
	Ideally all dialogs should inherits from this class. Dialogs are shown or
	hidden but never destroyed.
	"""

	def __init__(self, editor):
		"""
		Initialize basic dialog attributes and properties.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.

		@param window: An optional parent window.
		@type window: A gtk.Window object.
		"""
		Dialog.__init__(self)
		self.__init_attributes(editor)
		self.__set_dialog_properties()
		self.connect("key-press-event", self.__key_press_event_cb)
		self.connect("delete-event", self.__delete_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog attributes.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.

		@param window: A optional parent window.
		@type window: A gtk.Window object.
		"""
		self.editor = editor
		return

	def __set_dialog_properties(self):
		"""
		Set the default dialog properties.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
		"""
		self.set_property("has-separator", False)
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

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.
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
