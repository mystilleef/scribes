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

class SaveDialog(object):
	"""
	This class instantiates a dialog that allows clients to change the name of
	a file and save it. It inherites from ScribesDialog and the
	gtk.FileChooserDialog classes. See dialog.py and the GTK+ manual
	respectively for the properties of each class.
	"""

	def __init__(self, editor):
		"""
		Initialize the text editor's save dialog.

		@param self: Reference to the SaveDialog instance.
		@type self: A SaveDialog object.

		@param window: A possible parent window.
		@type window: A gtk.Window object.
		"""
		self.__init_attributes(editor)
		self.__set_dialog_properties()
		self.__signal_id_1 = self.__dialog.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_2 = self.__dialog.connect("response", self.__response_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog attributes.

		@param self: Reference to the ScribesOpenDialog instance.
		@type self: A ScribesOpenDialog object.

		@param window: A possible parent window.
		@type window: A gtk.Window object.
		"""
		self.__editor = editor
		from os.path import join, split
		cwd = split(globals()["__file__"])[0]
		glade_file = join(cwd, "Dialog.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, domain="scribes")
		self.__dialog = self.__glade.get_widget("SaveDialog")
		from SCRIBES.encodingbox import ScribesEncodingComboBox
		from SCRIBES.utils import create_encoding_box
		self.__encoding_box  = create_encoding_box(ScribesEncodingComboBox(editor))
		self.__status_id = None
		return

	def __set_dialog_properties(self):
		"""
		Set the dialog properties.

		@param self: Reference to the SaveDialog instance.
		@type self: A SaveDialog object.
		"""
		self.__dialog.set_extra_widget(self.__encoding_box)
		self.__dialog.set_transient_for(self.__editor.window)
		from gtk import RESPONSE_CANCEL, RESPONSE_OK, STOCK_SAVE, STOCK_CANCEL
		self.__dialog.add_button(STOCK_CANCEL, RESPONSE_CANCEL)
		self.__dialog.add_button(STOCK_SAVE, RESPONSE_OK)
		self.__dialog.set_default_response(RESPONSE_OK)
		self.__dialog.set_keep_above(True)
		from SCRIBES.dialogfilter import create_filter_list
		for filter in create_filter_list():
			self.__dialog.add_filter(filter)
		return

	def show_dialog(self):
		"""
		Show the text editor's open dialog.

		@param self: Reference to the SaveDialog instance.
		@type self: A SaveDialog object.
		"""
		self.__editor.response()
		self.__editor.emit("show-dialog", self.__dialog)
		from i18n import msg0002
		self.__status_id = self.__editor.feedback.set_modal_message(msg0002, "saveas")
		self.__set_current_folder_and_name()
		self.__editor.response()
		self.__dialog.show_all()
		self.__dialog.run()
		return

	def __hide(self):
		"""
		Hide dialog.

		@param self: Reference to the FileChooserDialog instance.
		@type self: A FileChooserDialog object.
		"""
		self.__editor.emit("hide-dialog", self.__dialog)
		self.__dialog.hide()
		if self.__status_id: self.__editor.feedback.unset_modal_message(self.__status_id)
		return

################################################################################
#
#					FIXME:
#
################################################################################

	def __set_current_folder_and_name(self):
		"""
		Set the current folder and name in the save dialog.

		@param self: Reference to the SaveDialog instance.
		@type self: A SaveDialog object.
		"""
		if self.__editor.uri:
			from gnomevfs import URI
			self.__dialog.set_current_folder_uri(str(URI(self.__editor.uri).parent))
			self.__dialog.set_current_name(str(URI(self.__editor.uri).short_name))
		else:
			from i18n import msg0003
			self.__dialog.set_current_name(msg0003)
			try:
				self.__dialog.set_current_folder(self.__editor.desktop_folder)
			except:
				self.__dialog.set_current_folder(self.__editor.home_folder)
		return

	def destroy_(self):
		self.__destroy_cb(self)
		return

	def __destroy_cb(self, dialog):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the SaveDialog instance.
		@type self: A SaveDialog object.

		@param dialog: Reference to the SaveDialog instance.
		@type dialog: A SaveDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__dialog)
		self.__dialog.destroy()
		del self
		self = None
		return

	def __delete_event_cb(self, *args):
		self.__hide()
		return

	def __response_cb(self, dialog, response_id):
		self.__hide()
		from operator import ne
		from gtk import RESPONSE_OK
		if ne(response_id, RESPONSE_OK): return
		newuri = self.__dialog.get_uri()
		self.__editor.emit("rename-document", newuri)
		return
