from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "error-data", self.__error_cb)
		self.connect(editor.window, "focus-in-event", self.__check_cb, True)
		self.connect(editor, "saved-file", self.__check_cb, True)
		self.connect(editor.textbuffer, "changed", self.__remove_cb, True)
		self.connect(manager, "start-check", self.__check_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__remove_timer()
		self.disconnect()
		del self
		return False

	def __recheck(self):
		self.__remove_timer()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(15000, self.__check_timeout, priority=PRIORITY_LOW)
		return False

	def __check(self):
		from Exceptions import RemoteFileError
		try:
			if self.__editor.window_is_active is False: raise ValueError
			if self.__is_local_file() is False: raise RemoteFileError
			self.__manager.emit("check")
		except ValueError:
			self.__recheck()
		except RemoteFileError:
			self.__remove_timer()
			self.__manager.emit("remote-file-error")
		return False

	def __is_local_file(self):
		uri = self.__editor.uri
		if not uri: return False
		if uri.startswith("file:///"): return True
		return False

	def __check_timeout(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__check, priority=PRIORITY_LOW)
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, *args):
		self.__remove_timer()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(1000, self.__check_timeout, priority=PRIORITY_LOW)
		return False

	def __error_cb(self, manager, data):
		if not data[0]: return False
		self.__recheck()
		return False

	def __remove_cb(self, *args):
		self.__remove_timer()
		return False
