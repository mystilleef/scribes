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

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

PRIORITY = 10
from gobject import GObject, SIGNAL_RUN_LAST, TYPE_STRING, TYPE_INT, TYPE_NONE

class OutputWriter(GObject):
	"""
	This class creates an object that writes files to local and remote
	locations.
	"""

	__gsignals__ = {
		"saved": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_INT,)),
		"error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_INT, TYPE_STRING, TYPE_INT)),
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
		self.__id = None
		self.__uri = None
		self.__swap_uri = None
		return

	def __reset_attributes(self):
		self.__id, self.__uri, self.__swap_uri = None, None, None
		return

	def __error(self, error_message, error_id):
		editor_id = self.__id
		self.__reset_attributes()
		self.emit("error", editor_id, error_message, error_id)
		return

	def write_file(self, editor_id, uri, text, swap_uri):
		from gnomevfs import OPEN_WRITE, URI
		from gnomevfs.async import create
		self.__id, self.__uri, self.__swap_uri = editor_id, uri, swap_uri
		try:
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
		#	self.__set_file_info()
			self.__finish_up()
		except:
			handle.cancel()
			self.__error("FileTransferUpdateError", 15)		return True

	def __finish_up(self):
		editor_id = self.__id
		self.__reset_attributes()
		self.emit("saved", editor_id)
		return
