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

class OpenDialog(object):
	"""
	This class instantiates a dialog that allows clients to select and load
	files into the text editor. It inherites from ScribesDialog and the
	gtk.FileChooserDialog classes. See dialog.py and the GTK+ manual
	respectively for the properties of each class.
	"""

	def __init__(self, editor):
		"""
		Initialize the text editor's open dialog.

		@param self: Reference to the OpenDialog instance.
		@type self: A OpenDialog object.

		@param window: A possible parent window.
		@type window: A gtk.Window object.
		"""
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = editor.connect("loaded-document", self.__reset_cb)
		self.__signal_id_2 = editor.connect("renamed-document", self.__reset_cb)
		self.__signal_id_3 = self.__dialog.connect("delete-event", self.__delete_event_cb)
		self.__signal_id_4 = self.__dialog.connect("response", self.__response_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog attributes.

		@param self: Reference to the OpenDialog instance.
		@type self: A OpenDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from os.path import join, split
		cwd = split(globals()["__file__"])[0]
		glade_file = join(cwd, "Dialog.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, domain="scribes")
		self.__dialog = self.__glade.get_widget("OpenDialog")
		from SCRIBES.encodingbox import ScribesEncodingComboBox
		from SCRIBES.utils import create_encoding_box
		self.__encoding_box  = create_encoding_box(ScribesEncodingComboBox(editor))
		self.__status_id = None
		self.__shortcut_folder_is_set = False
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = None
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the OpenDialog instance.
		@type self: A OpenDialog object.
		"""
		from gtk import STOCK_OPEN, STOCK_CANCEL, RESPONSE_OK, RESPONSE_CANCEL
		self.__dialog.add_button(STOCK_CANCEL, RESPONSE_CANCEL)
		self.__dialog.add_button(STOCK_OPEN, RESPONSE_OK)
		self.__dialog.set_extra_widget(self.__encoding_box)
		self.__dialog.set_default_response(RESPONSE_OK)
		self.__dialog.set_transient_for(self.__editor.window)
		self.__dialog.set_keep_above(True)
		from SCRIBES.dialogfilter import create_filter_list
		for filter in create_filter_list():
			self.__dialog.add_filter(filter)
		return

	def show_dialog(self):
		"""
		Show the text editor's open dialog.

		@param self: Reference to the OpenDialog instance.
		@type self: A OpenDialog object.
		"""
		self.__editor.response()
		self.__editor.emit("show-dialog", self.__dialog)
		from gobject import idle_add
		idle_add(self.__set_folder)
		from i18n import msg0002
		self.__status_id = self.__editor.feedback.set_modal_message(msg0002, "open")
		self.__editor.response()
		self.__dialog.show_all()
		self.__dialog.run()
		self.__editor.response()
		return

	def __hide(self):
		"""
		Hide dialog.

		@param self: Reference to the FileChooserDialog instance.
		@type self: A FileChooserDialog object.
		"""
		self.__editor.response()
		self.__editor.emit("hide-dialog", self.__dialog)
		self.__dialog.hide()
		if self.__status_id: self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__editor.response()
		return

	def __set_folder(self):
		self.__editor.response()
		from gobject import GError
		try:
			if not self.__editor.uri: return False
			if self.__shortcut_folder_is_set is False:
				from gnomevfs import URI
				self.__dialog.add_shortcut_folder_uri(str(URI(self.__editor.uri).parent))
				self.__shortcut_folder_is_set = True
		except GError:
			self.__shortcut_folder_is_set = True
		self.__dialog.select_uri(self.__editor.uri)
		self.__editor.response()
		return False

	def __reset_cb(self, *args):
		self.__shortcut_folder_is_set = False
		return

	def __response_cb(self, dialog, response_id):
		self.__hide()
		from operator import ne
		from gtk import RESPONSE_OK
		if ne(response_id, RESPONSE_OK): return
		# Load selected uri(s) into the text editor's buffer.
		uri_list = self.__dialog.get_uris()
		self.__editor.open_files(uri_list)
		return False

	def destroy_(self):
		self.__destroy()
		return

	def __destroy(self):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the OpenDialog instance.
		@type self: An OpenDialog object.

		@param dialog: Reference to the OpenDialog instance.
		@type dialog: An OpenDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__dialog)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__dialog)
		self.__dialog.destroy()
		self.__editor.delete_attributes(self)
		del self
		self = None
		return

	def __delete_event_cb(self, *args):
		self.__hide()
		return False
