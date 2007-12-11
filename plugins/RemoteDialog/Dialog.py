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

from gtk import Dialog
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class RemoteDialog(Dialog):
	"""
	This class creates a dialog used to open files at remote locations.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the remote dialog and set its state, behavior and properties.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Dialog.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__arrange_widgets()
		self.__signal_id_1 = self.__comboboxentry.child.connect("activate", self.__remote_activate_cb)
		self.__signal_id_2 = self.connect("delete", self.__destroy_cb)
		self.__signal_id_3 = self.connect("close", self.__close_cb)
		self.__signal_id_4 = self.connect("response", self.__response_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog's attributes.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__label = self.__create_labels()
		from comboboxentry import ScribesComboBoxEntry
		self.__comboboxentry = ScribesComboBoxEntry(editor)
		from SCRIBES.encodingbox import ScribesEncodingComboBox
		from SCRIBES.utils import create_encoding_box
		self.__encoding_box  = create_encoding_box(ScribesEncodingComboBox(editor))
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__status_id = None
		return

	def __set_properties(self):
		"""
		Set the dialog's properties.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.
		"""
		from i18n import msg0001
		self.set_property("title", msg0001)
		self.set_property("role", "scribes_remote_dialog")
		self.set_property("icon-name", "stock_open")
		self.set_property("name", "RemoteDialog")
		self.set_property("has-separator", False)
		self.set_property("skip-pager-hint", True)
		self.set_property("skip-taskbar-hint", True)
		self.set_property("urgency-hint", False)
		self.set_property("modal", True)
		from gtk import WIN_POS_CENTER_ON_PARENT
		self.set_property("window-position", WIN_POS_CENTER_ON_PARENT)
		self.set_property("resizable", True)
		from gtk import STOCK_OPEN, STOCK_CANCEL, RESPONSE_OK, RESPONSE_CANCEL
		self.add_button(STOCK_CANCEL, RESPONSE_CANCEL)
		self.add_button(STOCK_OPEN, RESPONSE_OK)
		self.set_default_response(RESPONSE_OK)
		self.set_property("border-width", 10)
		self.vbox.set_spacing(10)
		self.vbox.set_homogeneous(False)
		self.action_area.set_homogeneous(False)
		try:
			self.set_transient_for(self.__editor.window)
		except:
			pass
		return

	def __arrange_widgets(self):
		"""
		Arrange widgets after they have been created.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.
		"""
		self.vbox.pack_start(self.__label[0], True, True, 0)
		self.vbox.pack_start(self.__comboboxentry, True, True, 0)
		self.vbox.pack_start(self.__encoding_box, True, True, 0)
		return

	def show_dialog(self):
		"""
		Show the remote dialog.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.
		"""
		self.__editor.emit("show-dialog", self)
		from i18n import msg0002
		self.__status_id = self.__editor.feedback.set_modal_message(msg0002, "open")
		self.show_all()
		self.run()
		return

	def __hide_dialog(self):
		self.__editor.emit("hide-dialog", self)
		self.__editor.feedback.unset_modal_message(self.__status_id)
		self.hide()
		return

	def __create_labels(self):
		"""
		Create labels for the preferences dialog.

		@param self: Reference to the Preferences instance.
		@type self: A Preferences object.
		"""
		from i18n import msg0003
		string_list = [msg0003]
		label_list = []
		from gtk import Label
		# Convert strings to labels.
		for string in string_list:
			label = Label(string)
			label.set_use_underline(True)
			label.set_use_markup(True)
			label_list.append(label)
		return label_list

	def __remote_activate_cb(self, entry):
		"""
		Handles callback when the comboboxentry "activate" signal is emitted.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.

		@param entry: Text entry for the ScribesComboBoxEntry
		@type entry: A gtk.Entry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import RESPONSE_OK
		self.response(RESPONSE_OK)
		return True

	def __process_text_entry(self):
		"""
		Feed the URI provided in the text entry the text editor's loader object.

		@param self: Reference to the RemoteDialog instance.
		@type self: A RemoteDialog object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		text = self.__comboboxentry.child.get_text()
		if text: self.__editor.instance_manager.open_files([text.strip()])
		return False

	def __response_cb(self, dialog, response_id):
		self.__hide_dialog()
		from operator import eq, ne
		from gtk import RESPONSE_OK
		if ne(response_id, RESPONSE_OK): return False
		from gobject import idle_add
		idle_add(self.__process_text_entry)
		return False

	def __close_cb(self, *args):
		self.__hide_dialog()
		return False

	def __destroy_cb(self, dialog):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the ScribesDialog instance.
		@type self: A ScribesDialog object.

		@param dialog: Reference to the ScribesDialog instance.
		@type dialog: A ScribesDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__comboboxentry.child)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		self.__comboboxentry.emit("delete")
		self.destroy()
		del self
		self = None
		return
