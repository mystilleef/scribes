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

	def __init__(self, editor, encoding=None):
		"""
		Initialize object.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor, encoding)
		#self.__signal_id_1 = editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_1 = editor.connect("loaded-document", self.__loaded_document_cb)

	def __init_attributes(self, editor, encoding):
		"""
		Initialize data attributes.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__user_defined_encoding = encoding
		self.__determined_encoding = None
		self.__signal_id_1 = None
		self.__termination_id = editor.register_object()
		return

########################################################################
#
#						Public Methods
#
########################################################################

	def get_encoding(self, uri=None, string=None):
		"""
		Get the encoding for the file.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.

		@param uri: Reference to a file.
		@type uri: A String object.

		@param string: A string of characters
		@type string: A String object.

		@return: Return the encoding of the file.
		@rtype: A String object.
		"""
		from operator import truth
		if truth(self.__user_defined_encoding):
			encoding = self.__user_defined_encoding
		elif truth(uri):
			encoding = self.__get_encoding_from_database(uri)
			if truth(encoding):
				self.__determined_encoding = encoding
			else:
				encoding = "utf-8"
		elif truth(self.__determined_encoding):
			encoding = self.__determined_encoding
		else:
			encoding = "utf-8"
		return encoding

	def set_encoding(self, encoding):
		"""
		Set the encoding of the file.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.

		@param encoding: The encoding to set the file to.
		@type encoding: A String object.
		"""
		self.__user_defined_encoding = self.__determined_encoding = encoding
		return

	def destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		self.__set_encoding_in_database()
		self.__destroy()
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __get_encoding_from_database(self, uri):
		"""
		See if encoding data has been stored in the encoding database
		and get it if possible.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.

		@param uri: Reference to a file stored in the database.
		@type uri: A String object.

		@param encoding: Get encoding from database.
		@type encoding: A String object.
		"""
		# Get encoding stored in database, if any.
		from encoding_metadata import get_encoding_from_database
		encoding  = get_encoding_from_database(uri)
		return encoding

	def __set_encoding_in_database(self):
		"""
		Set encoding database.

		Only encodings other than UTF-8 are stored in the database.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		from operator import not_, contains, truth
		if not_(self.__editor.uri): return False
		default_encodings = ("utf8", "utf-8", "UTF-8", "UTF8", "Utf8", "Utf-8")
		user_defined = contains(default_encodings, self.__user_defined_encoding)
		determined_encoding = contains(default_encodings, self.__determined_encoding)
		if truth(self.__user_defined_encoding):# and not_(user_defined):
			from encoding_metadata import update_encoding_in_database
			update_encoding_in_database(str(self.__editor.uri), self.__user_defined_encoding)
		elif truth(self.__determined_encoding) and not_(determined_encoding):
			from encoding_metadata import update_encoding_in_database
			update_encoding_in_database(str(self.__editor.uri), self.__determined_encoding)
		return False

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the EncodingManager instance.
		@type self: A EncodingManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.unregister_object(self.__termination_id)
		del self
		self = None
		return

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

	def __loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the EncodingManager instance.
		@type self: An EncodingManager object.
		"""
		from gobject import idle_add
		idle_add(self.__set_encoding_in_database)
		return
