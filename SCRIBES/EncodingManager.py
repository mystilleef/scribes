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

class Manager(object):
	"""
	This class creates an object that manages encoding information for
	the text editor.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid2 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__renamed_file_cb)
		self.__sigid4 = editor.connect("quit", self.__quit_cb)
		self.__sigid5 = editor.connect("update-encoding-guess-list", self.__update_guess_list_cb)
		self.__sigid6 = editor.connect("new-encoding-list", self.__new_encoding_list_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__utf8_encodings = ["utf-8", "utf8", "UTF8", "UTF-8", "Utf-8"]
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __set_guess_list(self, encoding):
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

	def __set_encoding_list(self, new_encoding_list):
		from EncodingMetadata import set_value
		set_value(new_encoding_list)
		return False

	def __map_encoding_to_file(self, uri, encoding):
		from EncodedFilesMetadata import remove_value, set_value
		remove_value(uri) if encoding == "utf-8" else set_value(uri, encoding)
		return False

	def __format_encoding(self, encoding):
		# Remove white spaces. Convert to lower case.
		if encoding in self.__utf8_encodings: return "utf-8"
		return encoding.strip().lower()

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __quit_cb(self, *args):
		self.__destroy()
		return

	def __loaded_file_cb(self, editor, uri, encoding):
		if encoding is None: return
		encoding = self.__format_encoding(encoding)
		if encoding == "utf-8": return
		from thread import start_new_thread
		start_new_thread(self.__set_guess_list, (encoding,))
		return

	def __saved_file_cb(self, editor, uri, encoding):
		if encoding is None: return
		encoding = self.__format_encoding(encoding)
		from thread import start_new_thread
		start_new_thread(self.__map_encoding_to_file, (uri, encoding))
		return

	def __renamed_file_cb(self, editor, uri, encoding):
		encoding = "utf-8" if encoding is None else self.__format_encoding(encoding)
		from thread import start_new_thread
		start_new_thread(self.__map_encoding_to_file, (uri, encoding))
		start_new_thread(self.__set_guess_list, (encoding,))
		return

	def __update_guess_list_cb(self, editor, encoding):
		self.__set_guess_list(encoding)
		return False

	def __new_encoding_list_cb(self, editor, new_encoding_list):
		self.__set_encoding_list(new_encoding_list)
		return False
