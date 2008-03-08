# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that manages encoding information for
the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class EncodingManager(object):
	"""
	This class creates an object that manages encoding information for
	the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		#self.__signal_id_1 = editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_1 = editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_2 = editor.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_3 = editor.connect("renamed-document", self.__renamed_document_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__encoding = None
		self.__default_encoding = "utf-8"
		self.__utf8_encodings = ["utf-8", "utf8", "UTF8", "UTF-8", "Utf-8"]
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__termination_id = editor.register_object()
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __get_encoding(self):
		"""
		Return the encoding of a the document.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@return: Encoding of the file.
		@rtype: A String object.
		"""
		if self.__encoding: return self.__encoding
		return self.__default_encoding

	def __get_guess_list(self):
		"""
		Get a list of encodings that have been used to open a file.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		from EncodingGuessListMetadata import get_value
		return get_value()

	def __set_guess_list(self, encoding):
		"""
		Update the database with a list of encodings that have been used
		to successfully open a file.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param encoding: Encoding for a file.
		@type encoding: A String object.
		"""
		if encoding in [None, "utf-8"]: return False
		from EncodingGuessListMetadata import get_value, set_value
		encoding_list = get_value()
		if encoding_list:
			if encoding in encoding_list: return False
			encoding_list.append(encoding)
			set_value(encoding_list)
		else:
			set_value([encoding])
		return False

	def __get_encoding_list(self):
		"""
		Get list of encodings available in the open/save/remote dialog
		from the database.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		from EncodingMetadata import get_value
		return get_value()

	def __set_encoding_list(self, new_encoding_list):
		"""
		Update the database with list of selected encodings in the
		open/save/remote dialogs.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param new_encoding_list: A list of encodings
		@type new_encoding_list: A List object.
		"""
		from EncodingMetadata import set_value
		set_value(new_encoding_list)
		return False

	def __map_encoding_to_file(self, uri, encoding):
		"""
		Update the encoding of a file in a database.

		Database is never updated with "utf-8" encoding. The editor
		assumes files are "utf-8" by default.

		@param uri: Reference to a file.
		@type uri: A String object.

		@param encoding: Encoding of a file.
		@type encoding: A String object.
		"""
		from EncodedFilesMetadata import remove_value, set_value
		if encoding == "utf-8":
			remove_value(uri)
		else:
			set_value(uri, encoding)
		return False

	def __format_encoding(self, encoding):
		"""
		Remove white space and convert to lower case.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param encoding: Encoding of a file.
		@type encoding: A String object.

		@return: formatted encoding
		@rtype: A String object.
		"""
		# Remove white spaces. Convert to lower case.
		if encoding in self.__utf8_encodings: return self.__default_encoding
		return encoding.strip().lower()

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.unregister_object(self.__termination_id)
		del self
		self = None
		return

########################################################################
#
#						Public API
#
########################################################################

	encoding = property(__get_encoding)
	encoding_list = property(__get_encoding_list, __set_encoding_list)
	encoding_guess_list = property(__get_guess_list)

	def destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		self.__destroy()
		return

	def __precompile_methods(self):
		"""
		Tell psyco to optimize some methods.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		try:
			from psyco import bind
			bind(self.__saved_document_cb)
			bind(self.__map_encoding_to_file)
			bind(self.__format_encoding)
		except ImportError:
			pass
		return False

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __close_document_no_save_cb(self, *args):
		"""
		Handles callback when the "close-document-no-save" signal is emitted.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param *args: Irrelevant arguments.
		@type *args: A List object.
		"""
		self.__destroy()
		return

	def __loaded_document_cb(self, editor, uri, encoding):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		if encoding is None: return
		encoding = self.__format_encoding(encoding)
		if encoding in self.__default_encoding: return
		self.__encoding = encoding
		from gobject import idle_add
		idle_add(self.__set_guess_list, encoding, priority=5000)
		return

	def __saved_document_cb(self, editor, uri, encoding):
		"""
		Handles callback when the "saved-document" signal is emitted.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.
		"""
		if encoding is None: return
		encoding = self.__format_encoding(encoding)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__map_encoding_to_file, uri, encoding, priority=5000)
		if encoding in [self.__default_encoding, self.__encoding]: return
		self.__encoding = encoding
		return

	def __renamed_document_cb(self, editor, uri, encoding):
		"""
		Handles callback whent he "renamed-document" signal is emitted.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: Reference to file.
		@type uri: A String object.

		@param encoding: Encoding of file.
		@type encoding: A String object.
		"""
		self.__encoding = "utf-8" if encoding is None else self.__format_encoding(encoding)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__map_encoding_to_file, uri, self.__encoding, priority=5000)
		idle_add(self.__set_guess_list, self.__encoding, priority=5000)
		return
