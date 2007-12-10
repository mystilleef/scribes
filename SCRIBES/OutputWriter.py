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
This module documents a file that writes files to local and remote
locations.

@todo: Implement file info setting and getting.
@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

PRIORITY = 10
from gobject import GObject, SIGNAL_RUN_LAST, TYPE_PYOBJECT, TYPE_NONE

class OutputWriter(GObject):
	"""
	This class creates an object that writes files to local and remote
	locations.
	"""

	__gsignals__ = {
		"saved": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT, TYPE_PYOBJECT, TYPE_PYOBJECT)),
	}

	def __init__(self):
		"""
		Initialize object.

		@param self: Reference to the OutputWriter instance.
		@type self: An OutputWriter object.
		"""
		GObject.__init__(self)
		from gnome.ui import authentication_manager_init
		authentication_manager_init()
		self.__init_attributes()

	def __init_attributes(self):
		"""
		Iniitailize data attributes.

		@param self: Reference to the OutputWriter instance.
		@type self: An OutputWriter object.
		"""
		self.__id = None
		self.__uri = None
		self.__swap_uri = None
		self.__file_info = None
		return

	def write_file(self, editor_id, uri, text, swap_uri):
		"""
		Asyncronously write file to disk
		"""
		self.__reset_attributes()
		from gnomevfs import OPEN_WRITE, URI
		from gnomevfs.async import create
		self.__id, self.__uri, self.__swap_uri = editor_id, uri, swap_uri
		try:
			self.__file_info = self.__get_file_info()
			# Write to a temporary file.
			create(uri=URI(swap_uri),
					callback=self.__write_cb,
					open_mode=OPEN_WRITE,
					exclusive=False,
					perm=0644,
					priority=PRIORITY,
					data=text)
		except:
			self.__error("CreateError: Error while opening or creating file.", 11)
		return

	def __write_cb(self, handle, result, text):
		"""
		Callback to the GNOME-VFS asynchronous create method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			handle.write(text, self.__close_cb)
		except:
			handle.cancel()
			self.__error("WriteError: Error while writing file.", 12)
		return

	def __close_cb(self, handle, bytes, result, bytes_requested):
		"""
		Callback to the GNOME-VFS asynchronous write method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			handle.close(self.__finalize_cb)
		except:
			handle.cancel()
			self.__error("CloseError: Error while closing file", 13)
		return

	def __finalize_cb(self, *args):
		"""
		Callback to the GNOME-VFS asynchronous close method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		self.__begin_file_transfer()
		return

	def __begin_file_transfer(self):
		"""
		Transfer temporary file from swap location to permanent location.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from gnomevfs import XFER_OVERWRITE_MODE_REPLACE
		from gnomevfs import XFER_ERROR_MODE_QUERY, URI
		from gnomevfs.async import xfer
		XFER_TARGET_DEFAULT_PERMS = 1 << 12
		try:
			#raise Exception
			xfer(source_uri_list=[URI(self.__swap_uri)],
					target_uri_list=[URI(self.__uri)],
					xfer_options=XFER_TARGET_DEFAULT_PERMS,
					error_mode=XFER_ERROR_MODE_QUERY,
					priority = PRIORITY,
					overwrite_mode=XFER_OVERWRITE_MODE_REPLACE,
					progress_update_callback=self.__update_cb,
					update_callback_data=None,
					progress_sync_callback=self.__sync_cb)
		except:
			self.__error("BegineFileTransferError: Error while trying to transfer file", 14)
		return

	def __sync_cb(self, info):
		"""
		Callback the GNOME-VFS asynchronous transfer method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		if info.vfs_status: return False
		return  True

	def __update_cb(self, handle, info, data):
		"""
		Callback to the GNOME-VFS asynchronous transfer method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			if info.vfs_status: raise Exception
			from gnomevfs import XFER_PHASE_COMPLETED
			from operator import ne
			if ne(info.phase, XFER_PHASE_COMPLETED): return True
			self.__set_file_info()
			self.__finish_up()
		except:
			handle.cancel()
			self.__error("FileTransferUpdateError", 15)		return True

	def __finish_up(self):
		"""
		Last function call if save is successful.

		Emits save signal and resets attributes.

		@param self: Reference to the OutputWriter instance.
		@type self: An OutputWriter object.
		"""
		self.emit("saved", self.__id)
		return

	def __error(self, error_message, error_id):
		"""
		Emit error signal when an unexpected event occurs.

		@param self: Reference to the OutputWriter instance.
		@type self: An OutputWriter object.

		@param error_message: An error message.
		@type error_message: A String object.

		@param error_id: A number associated with an error.
		@type error_id: An Integer object.
		"""
		self.emit("error", self.__id, error_message, error_id)
		return

	def __get_file_info(self):
		"""
		Get file information about the file.

		@param self: Reference to the OutputWriter instance.
		@type self: A OutputWriter object.

		@return: An object containing file information.
		@rtype: A gnomevfs.FILE_INFO object.
		"""
		try:
			from operator import is_
			if is_(self.__uri.startswith("file:///"), False): return None
			from gnomevfs import get_file_info
			fileinfo = get_file_info(self.__uri)
		except:			return None		return fileinfo

	def __set_file_info(self):
		"""
		Set correct permissions of a file after it has been saved.

		@param self: Reference to the OutputWriter instance.
		@type self: A OutputWriter object.
		"""
		from operator import not_
		if not_(self.__file_info): return
		try:
			from gnomevfs import set_file_info, SET_FILE_INFO_PERMISSIONS
			set_file_info(self.__uri, self.__file_info, SET_FILE_INFO_PERMISSIONS)
		except:
			pass
		return

	def __reset_attributes(self):
		"""
		Reset object attributes to None.

		@param self: Reference to the OutputWriter instance.
		@type self: A OutputWriter object.
		"""
		self.__id, self.__uri, self.__swap_uri, self.__file_info = None, None, None, None
		return
