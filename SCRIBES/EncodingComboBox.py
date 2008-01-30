# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
#
# This file is part of SCRIBES.
#
# SCRIBES is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SCRIBES is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SCRIBES; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that creates a combo box used to choose
the encoding a file should be opened or saved with. The combobox is
found in the open/save/remote dialogs.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ComboBox

class EncodingComboBox(ComboBox):
	"""
	This class implements the encoding combo box for the open, save and
	remote dialog. The combo box contains a list of encodings a user
	can choose from to open or save a file with. The last item in the
	encoding box shows a window with a list of all the encodings
	the editor supports. Users can add more encodings to the combo box
	via the afore-mentioned window.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ComboBox.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__arrange_widgets()
		self.__sig_id_1 = self.connect("changed", self.__changed_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__update_encoding_list_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)
		#self.__populate_model()

	def __init_attributes(self, editor):
		"""
		Initialize object's attributes.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__sig_id_1 = self.__monitor_id_1 = None
		self.__model = self.__create_model()
		self.__encoding = None
		self.__window = None
		from utils import generate_encodings
		self.__encodings = generate_encodings()
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "Encoding.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __set_properties(self):
		"""
		Set properties.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		self.set_row_separator_func(self.__separator_function)
		return

	def __get_encoding(self):
		"""
		Get selected encoding.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		return self.__encoding

########################################################################
#
# 							PUBLIC API
#
########################################################################

	encoding = property(__get_encoding)

	def destroy_(self):
		"""
		Destroy combobox.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self)
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		if self.__window: self.__window.destroy()
		self.destroy()
		del self
		self = None
		return

########################################################################

	def __populate_model(self):
		"""
		Populate the combobox' model with encodings.

		@param self: Reference to the EncodingComboBox instance.
		@type self: A EncodingComboBox object.
		"""
		self.handler_block(self.__sig_id_1)
		self.__model.clear()
		from internationalization import msg0159, msg0158, msg0292
		self.__model.append([msg0292])
		self.__model.append(["Separator"])
		self.__model.append([msg0159])
		from EncodingMetadata import get_value
		encoding_list = get_value()
		for encoding in encoding_list:
			encoding = self.__create_encoding_for_display(encoding)
			if encoding is None: continue
			self.__model.append([encoding])
		self.__model.append(["Separator"])
		self.__model.append([msg0158])
		self.set_active(0)
		self.handler_unblock(self.__sig_id_1)
		return False

	def __create_encoding_for_display(self, encoding):
		"""
		Create string to be displayed in the encoding combobox.

		@param self: Reference to the EncodingComboBox instance.
		@type self: A EncodingComboBox object.

		@param encoding: An encoding to use to open or save a file.
		@type encoding: A String object.

		@return: A string to be displayed in the combobox representing an
			encoding.
		@rtype: A String object.
		"""
		message = None
		from operator import ne
		for items in self.__encodings:
			if ne(items[0], encoding): continue
			encoding, language = items[0], items[2]
			message = language + " (" + encoding + ")"
			break
		return message

	def __arrange_widgets(self):
		"""
		Arrange combobox with appropriate widgets.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		self.set_model(self.__model)
		from gtk import CellRendererText
		cell = CellRendererText()
		self.pack_end(cell, True)
		self.add_attribute(cell, "text", 0)
		return

	def __create_model(self):
		"""
		Create model for the combobox.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		from gtk import ListStore
		from gobject import TYPE_STRING
		model = ListStore(TYPE_STRING)
		return model

	def __separator_function(self, model, iterator):
		"""
		Draw a seperator at specific rows.

		This function is called for each row in the combobox' model.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.

		@param model: The model for the combobox.
		@type model: A gtk.ListStore object.

		@param iterator: An object pointing to a row in the model.
		@type iterator: A gtk.TreeIter object.

		@return: True to draw a separator, False otherwise.
		@rtype: A Boolean object.
		"""
		if model.get_value(iterator, 0) == "Separator" : return True
		return False

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
		from operator import ne
		for encoding in self.__encodings:
			if ne(encoding[0], string): continue
			encoding = encoding[1]
			break
		return encoding

	def __show_encoding_selection_window(self):
		"""
		Show encoding selection window.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.
		"""
		try:
			self.__window.show()
		except AttributeError:
			from EncodingSelectionWindow import EncodingSelectionWindow
			self.__window = EncodingSelectionWindow(self.__editor)
			self.__window.show()
		return

	def __changed_cb(self, *args):
		"""
		Handles callback when "changed" signal is emitted.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		from internationalization import msg0158, msg0159, msg0292
		if self.get_active_text() == msg0159:
			self.__encoding = "utf-8"
		elif self.get_active_text() == msg0158:
			self.__show_encoding_selection_window()
			self.handler_block(self.__sig_id_1)
			self.set_active(0)
			self.handler_unblock(self.__sig_id_1)
		elif self.get_active_text() == msg0292:
			self.__encoding = None
		else:
			self.__encoding = self.__get_encoding_from_combobox(self.get_active_text())
		return True

	def __update_encoding_list_cb(self, *args):
		"""
		Update the combobox when encodings are added or removed to its list.

		@param self: Reference to the EncodingComboBox instance.
		@type self: An EncodingComboBox object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)
		return
