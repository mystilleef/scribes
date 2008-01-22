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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module defines a class that loads a file into the editor's buffer.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class FileLoader(object):
	"""
	This class creates an object that loads a file into the editor's
	buffer.
	"""

	def __init__(self, editor, uri, encoding="utf-8", readonly=False):
		"""
		Initialize object.

		@param self: Reference to the FileLoader instance.
		@type self: A FileLoader object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A file to open.
		@type uri: A FileLoader object.

		@param readonly: Toggle readonly.
		@type readonly: A Boolean object.
		"""
		try:
			editor.emit("checking-document", uri)
			from Exceptions import PermissionError
			from Exceptions import AccessDeniedError, FileInfoError
			from Exceptions import NotFoundError
			self.__init_attributes(editor, uri, encoding, readonly)
			self.__get_file_info()
			self.__verify_permissions()
			self.__load_uri()
		except PermissionError:
			from internationalization import msg0479
			self.__error(msg0479)
		except AccessDeniedError:
			from internationalization import msg0480
			self.__error(msg0480)
		except FileInfoError:
			from internationalization import msg0481
			self.__error(msg0481)
		except NotFoundError:
			from internationalization import msg0482
			self.__error(msg0482)
		except:
			from internationalization import msg0483
			self.__error(msg0483)

	def __init_attributes(self, editor, uri, encoding, readonly):
		"""
		Initialize data attributes.

		@param self: Reference to the FileLoader instance.
		@type self: A FileLoader object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A file to open.
		@type uri: A FileLoader object.

		@param readonly: Toggle readonly.
		@type readonly: A Boolean object.
		"""
		self.__encoding = encoding
		self.__editor = editor
		self.__uri = uri
		self.__readonly = readonly
		self.__handle = None
		self.__temp_buffer = ""
		self.__writable_vfs_schemes = ["ssh", "sftp", "smb", "dav", "davs", "ftp"]
		return

	def __get_file_info(self):
		"""
		Get file information for remote files.

		@param self: Reference to the FileLoader instance.
		@type self: A FileLoader object.
		"""
		try:
			if self.__uri.startswith("file:///"): return
			self.__editor.init_authentication_manager()
			FILE_INFO_ACCESS_RIGHTS = 1 << 4
			from gnomevfs import AccessDeniedError, NotFoundError
			from gnomevfs import get_file_info, FILE_INFO_DEFAULT
			from gnomevfs import FILE_INFO_GET_MIME_TYPE
			from gnomevfs import FILE_INFO_FORCE_SLOW_MIME_TYPE
			from gnomevfs import FILE_INFO_FOLLOW_LINKS#, FILE_INFO_GET_ACCESS_RIGHTS
			fileinfo = get_file_info(self.__uri, FILE_INFO_DEFAULT |
										FILE_INFO_GET_MIME_TYPE |
										FILE_INFO_FORCE_SLOW_MIME_TYPE |
										FILE_INFO_FOLLOW_LINKS |
										FILE_INFO_ACCESS_RIGHTS)
			if not fileinfo:
				from Exceptions import FileInfoError
				raise FileInfoError
		except AccessDeniedError:
			from Exceptions import AccessDeniedError
			raise AccessDeniedError
		except NotFoundError:
			from Exceptions import NotFoundError
			raise NotFoundError
		except:
			from Exceptions import FileInfoError
			raise FileInfoError
		return

	def __verify_permissions(self):
		"""
		Check if user has permission to view the file.

		@param self: Reference to the FileLoader instance.
		@type self: A FileLoader object.
		"""
		if self.__uri.startswith("file:///"):
			from gnomevfs import get_local_path_from_uri
			local_path = get_local_path_from_uri(self.__uri)
			from os import access, W_OK, R_OK
			if access(local_path, R_OK):
				if not access(local_path, W_OK):
					self.__readonly = True
			else:
				from Exceptions import PermissionError
				raise PermissionError
		else:
			from gnomevfs import get_uri_scheme
			scheme = get_uri_scheme(self.__uri)
			if not scheme in self.__writable_vfs_schemes:
				self.__readonly = True
		return

	def __load_uri(self):
		"""
		Load file.

		@param self: Reference to the FileLoader instance.
		@type self: A FileLoader object.
		"""
		self.__editor.emit("loading-document", self.__uri)
		from gnomevfs import OPEN_READ, URI
		from gnomevfs.async import open
		try:
			open(URI(self.__uri), self.__open_cb, OPEN_READ, 10)
		except:
			from Exceptions import OpenFileError
			from internationalization import msg0484
			self.__error(msg0484)
		return

	def __open_cb(self, handle, result):
		"""
		Handles callback to read a URI after it has been opened asynchronously.

		This function reads the contents of a URI. If the URI is local, it reads
		all its content. If the URI is remote, the contents of the URI is read
		4096 bytes at a time.

		@param self: Reference to the Loader instance.
		@type self: A Loader object.

		@param handle: An object pointing to a URI.
		@type handle: A gnomevfs.Handle object.

		@param result: The result of a read operation.
		@type result: A gnomevfs.Error object.
		"""
		from Exceptions import ReadFileError
		try:
			self.__handle = handle
			if self.__uri.startswith("file:///"):
				try:
					from gnomevfs import get_local_path_from_uri
					local_path = get_local_path_from_uri(self.__uri)
					from os.path import getsize
					from operator import not_
					size = getsize(local_path)
					if not_(size): size = 4096
					handle.read(size, self.__read_cb)
				except:
					raise ReadFileError
			else:
				try:
					handle.read(4096, self.__read_cb)
				except:
					raise ReadFileError
		except ReadFileError:
			from internationalization import msg0485
			self.__error(msg0485)
		return

	def __read_cb(self, handle, buffer, result, bytes):
		"""
		Handles callback to insert text into the editor's buffer.

		@param self: Reference to the Loader instance.
		@type self: A Loader object.

		@param handle:
		@type handle: A gnomevfs.Handle object.

		@param buffer: An area in memory where text read from a URI is placed.
		@type buffer: A String object.

		@param result: The result of a read operation.
		@type result: A gnomevfs.Error object.

		@param bytes: Bytes read.
		@type bytes: An Integer object.
		"""
		try:
			from Exceptions import CloseFileError, ReadFileError
			from Exceptions import GnomeVfsError
			from gnomevfs import EOFError
			from operator import is_, eq, contains, not_
			if self.__uri.startswith("file:///"):
				if not_(contains((None, EOFError), result)): raise GnomeVfsError
				self.__insert_string_to_buffer(buffer, handle)
				try:
					handle.close(self.__close_cb)
				except:
					raise CloseFileError
			else:
				if is_(result, None):
					try:
						self.__temp_buffer += buffer
						handle.read(4096, self.__read_cb)
					except:
						raise ReadFileError
				elif eq(result, EOFError):
					try:
						self.__insert_string_to_buffer(self.__temp_buffer, handle)
						handle.close(self.__close_cb)
					except:
						raise ReadFileError
				else:
					raise GnomeVfsError
		except CloseFileError:
			from internationalization import msg0486
			self.__error(msg0486)
		except ReadFileError:
			from internationalization import msg0485
			self.__error(msg0485)
		except GnomeVfsError:
			self.__error("GnomeVfsError")
		return

	def __close_cb(self, *args):
		"""
		Close the URI and finalize the editor's buffer for editing.

		@param self: Reference to the Loader instance.
		@type self: A Loader object.
		"""
		self.__editor.emit("loaded-document", self.__uri, self.__encoding)
		if self.__readonly: self.__editor.emit("enable-readonly")
		self.__destroy()
		return

	def __insert_string_to_buffer(self, string, handle=None):
		"""
		Insert text into the editor's buffer.

		@param self: Reference to the Loader instance.
		@type self: A Loader object.

		@param string: Text to insert into the text editor's buffer.
		@type string: A String object.

		@param handle: An object pointing to a remote URI.
		@type handle: A gnomevfs.Handle object.
		"""
		try:
			self.__encoding = self.__determine_encoding()
			encoding_list = self.__editor.encoding_guess_list
			if encoding_list:
				encoding_list.insert(0, self.__encoding)
				success = False
				for encoding in encoding_list:
					try:
						unicode_string = string.decode(encoding)
						success = True
						break
					except UnicodeDecodeError:
						continue
				if success is False: raise ValueError
			else:
				try:
					unicode_string = string.decode(self.__encoding)
				except TypeError:
					unicode_string = string.decode("utf-8")
			utf8_string = unicode_string.encode("utf-8")
			self.__editor.textbuffer.set_text(utf8_string)
		except UnicodeDecodeError:
			from internationalization import msg0487
			self.__error(msg0487)
		except ValueError:
			from internationalization import msg0487
			self.__error(msg0487)
		except UnicodeEncodeError:
			from internationalization import msg0488
			self.__error(msg0488)
		return

	def __determine_encoding(self):
		if self.__encoding: return self.__encoding
		from EncodedFilesMetadata import get_value
		encoding_from_file = get_value(self.__uri)
		if encoding_from_file is None and self.__encoding is None: return "utf-8"
		if encoding_from_file: return encoding_from_file
		if self.__encoding is None: return "utf-8"
		return "utf-8"

	def __error(self, message):
		"""
		Show an error message

		@param message: A message describing an error:
		@type message: A String object.
		"""
		try:
			if self.__handle: self.__handle.cancel()
			from internationalization import msg0477, msg0478
			from gnomevfs import format_uri_for_display
			title = msg0477 % (format_uri_for_display(self.__uri))
			message_id = self.__editor.feedback.set_modal_message(msg0478, "error")
			self.__editor.show_error_message(message, title, self.__editor.window)
			self.__editor.emit("load-error", self.__uri)
			self.__editor.feedback.unset_modal_message(message_id)
			self.__destroy()
		except AttributeError:
			pass
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the FileLoader instance.
		@type self: A FileLoader object.
		"""
		del self
		self = None
		return
