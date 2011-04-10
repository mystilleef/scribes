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
		self.__remove_all_timers()
		self.disconnect()
		del self
		return False

	def __recheck(self):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(30000, self.__check_timeout, priority=PRIORITY_LOW)
		return False

	def __check(self):
		from Exceptions import RemoteFileError
		try:
			from gobject import idle_add, PRIORITY_LOW
			if self.__editor.window_is_active is False: raise ValueError
			if self.__is_local_file() is False: raise RemoteFileError
			idle_add(self.__manager.emit, "check", priority=PRIORITY_LOW)
		except ValueError:
			idle_add(self.__recheck, priority=PRIORITY_LOW)
		except RemoteFileError:
			self.__remove_timer()
			idle_add(self.__manager.emit, "remote-file-error", priority=PRIORITY_LOW)
		return False

	def __is_local_file(self):
		uri = self.__editor.uri
		if not uri: return False
		if uri.startswith("file:///"): return True
		return False

	def __check_timeout(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__check, priority=PRIORITY_LOW)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
				3: self.__timer3,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 4)]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, *args):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer3 = timeout_add(3000, self.__check_timeout, priority=PRIORITY_LOW)
		return False

	def __error_cb(self, manager, data):
		if not data[0]: return False
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__recheck, priority=PRIORITY_LOW)
		return False

	def __remove_cb(self, *args):
		self.__remove_all_timers()
		return False
