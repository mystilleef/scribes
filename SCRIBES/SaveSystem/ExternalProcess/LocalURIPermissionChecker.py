class Checker(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("check-permission", self.__check_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __check(self, data):
		try:
			uri = data[1]
			if not uri.startswith("file:///"): raise StandardError
			from gnomevfs import get_local_path_from_uri
			file_path = get_local_path_from_uri(uri)
			from os import access, W_OK, path
			folder_path = path.dirname(file_path)
			if access(folder_path, W_OK) is False: raise ValueError
			elif access(file_path, W_OK) is False and path.exists(file_path): raise ValueError
			self.__manager.emit("encode-text", data)
		except StandardError:
			self.__manager.emit("encode-text", data)
		except ValueError:
			from gettext import gettext as _
			message = _("""
Module: SCRIBES/SaveSystem/ExternalProcess/LocalURIPermissionChecker.py 
Class: Checker
Method: __check 
Exception: Unknown
Error: You do not have permission to write to save location.

Automatic saving is temporarily disabled. You will loose information in
this window if you close it. Please try saving the file again, preferably
to a different location like your desktop.""")
			data = data + (message,)
			self.__manager.emit("oops", data)
		return False

	def __check_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__check, data)
		return False
