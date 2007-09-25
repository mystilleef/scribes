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
A custom generic dialog for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Window

class Dialog(Window):
	"""
	This class creates a dialog for the text editor. The class is
	designed primarily for inheritance.
	"""

	def __init__(self):
		"""
		Initialize the dialog.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.
		"""
		Window.__init__(self)
		self.__init_attributes()
		self.__set_properties()
		self.__arrange_widgets()
		self.connect("key-press-event", self.__window_key_press_event_cb)
		self.connect("delete-event", self.__window_delete_event_cb)
		self.cancel_button.connect("clicked", self.__window_clicked_cb)

	def __init_attributes(self):
		"""
		Initialize the dialog's data attributes.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.
		"""
		from gtk import VBox, HButtonBox, Button, STOCK_CANCEL
		self.main_area = VBox()
		self.button_area = HButtonBox()
		self.spacing = 10
		self.cancel_button = Button(stock=STOCK_CANCEL, use_underline=True)
		return

	def __set_properties(self):
		"""
		Define the dialog's default properties and behavior.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.
		"""
		from gtk import WIN_POS_CENTER_ON_PARENT
		from gtk.gdk import WINDOW_TYPE_HINT_DIALOG, GRAVITY_CENTER
		self.set_type_hint(WINDOW_TYPE_HINT_DIALOG)
		self.set_property("role", "Scribes Base Dialog")
		self.set_property("name", "Scribes Dialog")
		self.set_property("title", "Scribes Dialog")
		self.set_property("modal", True)
		self.set_property("skip-taskbar-hint", True)
		self.set_property("skip-pager-hint", True)
		self.set_property("icon-name", "gnome-settings")
		self.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		self.set_property("resizable", True)
		self.set_property("border-width", self.spacing)
		self.main_area.set_spacing(self.spacing)
		self.button_area.set_spacing(self.spacing)
		from gtk import BUTTONBOX_END
		self.button_area.set_property("layout-style", BUTTONBOX_END)
		return

	def __arrange_widgets(self):
		"""
		Arrange the widgets for the dialog.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.
		"""
		from gtk import VBox
		vbox = VBox(spacing=self.spacing)
		self.add(vbox)
		vbox.pack_start(self.main_area, True, True, 0)
		vbox.pack_start(self.button_area, False, False, 0)
		return

	def show_dialog(self):
		"""
		Show the dialog.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.
		"""
		self.show_all()
		return

	def hide_dialog(self):
		"""
		Hide the dialog.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.
		"""
		self.hide()
		return

	def __window_key_press_event_cb(self, dialog, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.

		@param dialog: Reference to the Dialog
		@type dialog: A Dialog object.

		@param event: An event that occurs when the keyboard is pressed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import keysyms
		if event.keyval == keysyms.Escape:
			self.hide_dialog()
			return True
		return False

	def __window_delete_event_cb(self, dialog, event):
		"""
		Handles callback when the "delete-event" signal is emitted.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.

		@param dialog: Reference to the Dialog.
		@type dialog: A Dialog object.

		@param event: An event that occurs when the dialog window is closed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.hide_dialog()
		return True

	def __window_clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the Dialog instance.
		@type self: A Dialog object.

		@param button: The dialog's cancel button
		@type button: A gtk.Button object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.hide_dialog()
		return True

	def error_message(self, message, secondary_message=None):
		"""
		Show an error dialog with a message.

		@param self: Reference to the TemplateAddDialog instance.
		@type self: A TemplateAddDialog object.

		@param message: An error message.
		@type message: A String object.
		"""
		from gtk import MessageDialog, DIALOG_DESTROY_WITH_PARENT
		from gtk import MESSAGE_ERROR, BUTTONS_CLOSE
		dialog = MessageDialog(parent=self, flags=DIALOG_DESTROY_WITH_PARENT,
			type=MESSAGE_ERROR, buttons=BUTTONS_CLOSE,
			message_format=None)
		dialog.format_secondary_text(message)
		from internationalization import msg0133
		dialog.set_property("title", msg0133)
		dialog.set_property("role", "error_message_dialog")
		dialog.set_property("icon-name", "stock_dialog-error")
		dialog.set_property("skip-pager-hint", True)
		dialog.set_property("skip-taskbar-hint", True)
		dialog.set_property("urgency-hint", False)
		dialog.set_property("modal", True)
		from gtk import WIN_POS_CENTER_ON_PARENT
		dialog.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		dialog.set_property("resizable", True)
		dialog.run()
		dialog.hide_all()
		dialog.destroy()
		return
