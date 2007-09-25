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
# along with ${project_name}; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gtk import ComboBox

class ScribesEncodingComboBox(ComboBox):
	"""
	This class implements the encoding combobox for the text editor's open
	dialog. It inherits from gtk.ComboBox. The encoding combobox presents a list
	of encodings that can be used to open text documents. The text editor will
	default to the UTF-8 encoding if no encoding is selected by the user.
	"""

	def __init__(self, editor):
		"""
		Initialize the encoding combobox object.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param opendialog: The text editor's open dialog.
		@type opendialog: A ScribesOpenDialog object.
		"""
		ComboBox.__init__(self)
		self.__init_attributes(editor)
		self.__setup_combobox_widgets()
		self.__populate_liststore()
		self.set_row_separator_func(self.__separator_function)
		self.connect("changed", self.__combobox_cb)
		# Notify the combobox when the encoding list in the GConf database is
		# updated.
		self.client.notify_add("/apps/scribes/encodings",
							self.__update_encoding_list_cb, self)

	def __init_attributes(self, editor):
		"""
		Initialize the combobox' attributes

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param opendialog: The text editor's open dialog.
		@type opendialog: A ScribesOpenDialog object.
		"""
		self.editor = editor
		self.model = self.__create_liststore()
		self.client = editor.gconf_client
		from utils import generate_encodings
		self.encodings = generate_encodings()
		return

	def __create_liststore(self):
		"""
		Create a ListStore object for the combobox.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@return: A database, or model, for the combobox containing a list of
			encodings.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		from gobject import TYPE_STRING
		model = ListStore(TYPE_STRING)
		return model

	def __setup_combobox_widgets(self):
		"""
		Create widgets for the combobox object.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.
		"""
		self.set_model(self.model)
		from gtk import CellRendererText
		cell = CellRendererText()
		self.pack_end(cell, True)
		self.add_attribute(cell, "text", 0)
		return

	def __populate_liststore(self):
		"""
		Populate the combobox' model with encodings.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.
		"""
		self.model.clear()
		from internationalization import msg0159, msg0158, msg0292
		self.model.append([msg0292])
		self.model.append(["Separator"])
		self.model.append([msg0159])
		from gconf import VALUE_STRING
		encoding_list = self.client.get_list("/apps/scribes/encodings",
											VALUE_STRING)
		for encoding in encoding_list:
			encoding = self.__create_encoding_for_display(encoding)
			if encoding is None:
				continue
			self.model.append([encoding])
		self.model.append(["Separator"])
		self.model.append([msg0158])
		self.set_active(0)
		return False

	def __create_encoding_for_display(self, encoding):
		"""
		Create string to be displayed in the encoding combobox.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param encoding: An encoding to use to open or save a file.
		@type encoding: A String object.

		@return: A string to be displayed in the combobox representing an
			encoding.
		@rtype: A String object.
		"""
		message = None
		for items in self.encodings:
			if items[0] == encoding:
				encoding, language = items[0], items[2]
				message = language + " (" + encoding + ")"
				break
		return message

	def __separator_function(self, model, iterator):
		"""
		Draw a seperator at specific rows.

		This function is called for each row in the combobox' model.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param model: The model for the combobox.
		@type model: A gtk.ListStore object.

		@param iterator: An object pointing to a row in the model.
		@type iterator: A gtk.TreeIter object.

		@return: True to draw a separator, False otherwise.
		@rtype: A Boolean object.
		"""
		if model.get_value(iterator, 0) == "Separator" :
			return True
		return False

	def __update_encoding_list_cb(self, client, cnxn_id, entry, data):
		"""
		Update the combobox when encodings are added or removed to its list.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param client: An object that provides access to the GConf database via
			a daemon.
		@type client: A gconf.Client object.

		@param cnxn_id: ?
		@type cnxn_id: An Integer object.

		@param entry: ?
		@type entry: A gconf.Entry object.
		"""
		from gobject import timeout_add
		timeout_add(3, self.__populate_liststore)
		return True

	def __combobox_cb(self, combobox):
		"""
		Handles callback when items in combobox changes.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param combobox: A reference to the combobox object holding a list of
			encodings
		@type combobox: A gtk.ComboBox object
		"""
		manager = self.editor.get_object("EncodingManager")
		from gobject import timeout_add
		from internationalization import msg0158, msg0159, msg0292
		if self.get_active_text() == msg0159:
			manager.set_encoding("utf-8")
		elif self.get_active_text() == msg0158:
			# Show the encoding dialog when the Add or Remove item is selected.
			from encodingdialog import ScribesEncodingDialog
			try:
				self.encodingdialog.show_dialog()
			except:
				self.encodingdialog = ScribesEncodingDialog(self.editor)
				self.encodingdialog.show_dialog()
			timeout_add(3, self.__populate_liststore)
		elif self.get_active_text() == msg0292:
			manager.set_encoding("utf-8")
		else:
			encoding = self.__get_encoding_from_combobox(self.get_active_text())
			manager.set_encoding(encoding)
		return True

	def __get_encoding_from_combobox(self, string):
		"""
		Determine the encoding selected from the combobox list.

		@param self: Reference to the ScribesEncodingComboBox instance.
		@type self: A ScribesEncodingComboBox object.

		@param string: A string representing an encoding
		@type string: A String object.
		"""
		from re import UNICODE, findall
		match = findall(r"\(.+\)", string, UNICODE)
		string = match[0].strip("()")
		for encoding in self.encodings:
			if encoding[0] == string:
				encoding = encoding[1]
				break
		return encoding
