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
This module documents as class that saves files to a local or remote
location.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class OutputProcessor(object):
	"""
	This class creates an instance that saves files to local or remote
	locations.
	"""

	def __init__(self, dbus):
		"""
		Initialize this object.

		@param self: Reference to the OutputProcessor instance.
		@type self: An OutputProcessor object.
		"""
		self.__init_attributes(dbus)
		self.__signal_id_1 = self.__writer.connect("saved", self.__saved_cb)
		self.__signal_id_2 = self.__writer.connect("error", self.__error_cb)

	def __init_attributes(self, dbus):
		self.__dbus = dbus
		self.__file_dictionary = {}
		from collections import deque
		self.__queue = deque([])
		self.__is_busy = False
		self.__swap_folder = None
		from OutputWriter import OutputWriter
		self.__writer = OutputWriter()
		return

	def process(self, editor_id, text, uri, encoding):
		try:
			if self.__is_busy: raise ValueError
			self.__is_busy = True
			from Exceptions import PermissionError, SwapError
			self.__check_permissions(uri)
			swap_file_uri = self.__get_swap_file(editor_id)
			encoded_text = self.__encode_text(text, encoding)
			self.__save_file(editor_id, uri, encoded_text, swap_file_uri)
		except ValueError:
			self.__queue.append((editor_id, text, uri, encoding))
		except PermissionError:
			print "PermissionError"
		except UnicodeEncodeError:
			print "UnicodeEncodeError"
		except UnicodeDecodeError:
			print "UnicodeDecodeError"
		except SwapError:
			print "SwapError"
		return

	def update(self, editor_id):
		try:
			swap_file = self.__file_dictionary[editor_id]
			from gnomevfs import unlink
			unlink(swap_file)
		except KeyError:
			pass
		return

	def __check_permissions(self, uri):
		from operator import not_, is_
		if not_(uri.startswith("file:///")): return
		from gnomevfs import get_local_path_from_uri
		file_path = get_local_path_from_uri(uri)
		from os import access, W_OK, path
		folder_path = path.dirname(file_path)
		from Exceptions import PermissionError
		if is_(access(folder_path, W_OK), False):
			raise PermissionError		elif is_(access(file_path, W_OK), False):
			if path.exists(file_path): raise PermissionError
		return

	def __get_swap_file(self, editor_id):
		from operator import contains
		if contains(self.__file_dictionary.keys(), editor_id): return self.__file_dictionary[editor_id]
		swap_uri = self.__create_swap_file(self.__create_swap_folder())
		self.__file_dictionary[editor_id] = swap_uri
		return swap_uri

	def __create_swap_file(self, folder):
		# Create a temporary folder.
		from tempfile import NamedTemporaryFile
		try:
			# Create a randomly generated temporary file in the
			# temporary folder created above.
			swap_file = NamedTemporaryFile(mode="w+",
												suffix="Scribes",
												prefix="scribes",
												dir=self.__swap_folder)
			from gnomevfs import get_uri_from_local_path
			swap_uri = get_uri_from_local_path(swap_file.name)
		except:
			from Exceptions import SwapError
			raise SwapError
		return swap_uri

	def __create_swap_folder(self):
		from os import path
		if self.__swap_folder and path.exists(self.__swap_folder): return self.__swap_folder
		from tempfile import mkdtemp
		from info import home_folder
		try:
			self.__swap_folder = mkdtemp(suffix="scribes",
										prefix=".Scribes",
										dir=home_folder)
		except:
			from Exceptions import SwapError
			raise SwapError
		return self.__swap_folder

	def __encode_text(self, text, encoding):
		encoded_text = text.encode(encoding)
		return encoded_text

	def __save_file(self, editor_id, uri, text, swap_uri):
		self.__writer.write_file(editor_id, uri, text, swap_uri)
		return

	def __destroy(self):
		from utils import disconnect_signal
		disconnect_signal(self.__signal_id_1, self.__writer)
		disconnect_signal(self.__signal_id_2, self.__writer)
		self.__file_dictionary.clear()
		self.__queue.clear()
		del self
		self = None
		return

	def __error(self, editor_id, error_message, error_id):
		self.__is_busy = False
		self.__dbus.error(editor_id, error_message, error_id)
		return

	def __saved_cb(self, writer, editor_id):
		try:
			self.__dbus.saved_file(editor_id)
			self.__is_busy = False
			editor_id, text, uri, encoding = self.__queue.popleft()
			self.process(editor_id, text, uri, encoding)
		except IndexError, ValueError:
			pass
		return

	def __error_cb(self, writer, editor_id, error_message, error_id):
		self.__error(editor_id, error_message, error_id)
		return
