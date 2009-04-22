PRIORITY = 10
from gettext import gettext as _

class Writer(object):

	def __init__(self, manager):
		from gnome.ui import authentication_manager_init
		authentication_manager_init()
		self.__init_attributes(manager)
		manager.connect("write-to-swap-file", self.__write_swap_file_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__data = ()
		self.__file_info = None
		return

	def __get_file_info(self, uri):
		try:
			if uri.startswith("file:///") is False: return None
			from gnomevfs import get_file_info, URI
			fileinfo = get_file_info(URI(uri))
		except:
			return None
		return fileinfo

	def __error(self, message):
		data = self.__data + (message,)
		self.__manager.emit("oops", data)
		return False

	def __write(self, data):
		try:
			from gnomevfs import OPEN_WRITE, URI
			from gnomevfs.async import create
			# data = (session_id, uri, encoding, text, swapfile)
			self.__data = data
			uri, text, swapfile = data[1], data[3], data[4]
			self.__file_info = self.__get_file_info(uri)
			create(uri=URI(swapfile),
					callback=self.__write_cb,
					open_mode=OPEN_WRITE,
					exclusive=False,
					perm=0644,
					priority=PRIORITY,
					data=text)
		except:
			message = _("""
Module: SCRIBES/SaveSystem/ExternalProcess/SwapFileWriter.py
Class: Writer
Method: __write
Exception: Unknown
Error: Failed to open swap file for writing.

Automatic saving is temporarily disabled. You will loose information in
this window if you close it. Please try saving the file again, preferably
to a different location like your desktop.""")
			self.__error(message)
		return False

	def __write_cb(self, handle, result, text):
		try:
			handle.write(text, self.__close_cb)
		except:
			handle.cancel()
			message = _("""
Module: SCRIBES/SaveSystem/ExternalProcess/SwapFileWriter.py
Class: Writer
Method: __write_cb
Exception: Unknown
Error: Failed to write to swap file.

Automatic saving is temporarily disabled. You will loose information in
this window if you close it. Please try saving the file again, preferably
to a different location like your desktop.""")
			self.__error(message)
		return

	def __close_cb(self, handle, bytes, result, bytes_requested):
		try:
			handle.close(self.__finalize_cb)
		except:
			handle.cancel()
			message = _("""
Module: SCRIBES/SaveSystem/ExternalProcess/SwapFileWriter.py
Class: Writer
Method: __close_cb
Exception: Unknown
Error: Failed to close swap file after writing.

Automatic saving is temporarily disabled. You will loose information in
this window if you close it. Please try saving the file again, preferably
to a different location like your desktop.""")
			self.__error(message)
		return

	def __finalize_cb(self, *args):
		data = self.__data
		# data = (session_id, uri, encoding, swapfile, fileinfo)
		data = data[0], data[1], data[2], data[4], self.__file_info
		self.__manager.emit("transfer", data)
		return

	def __write_swap_file_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__write, data)
		return False
