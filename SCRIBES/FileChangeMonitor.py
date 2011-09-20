from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "close", self.__close_cb)
		self.connect(editor, "loaded-file", self.__monitor_cb, True)
		self.connect(editor, "renamed-file", self.__monitor_cb, True)
		self.connect(editor, "save-file", self.__busy_cb)
		self.connect(editor, "rename-file", self.__busy_cb)
		self.connect(editor, "save-error", self.__nobusy_cb, True)
		self.connect(editor, "saved-file", self.__nobusy_cb, True)
		self.connect(editor, "saved-file", self.__saved_file_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__uri = ""
		self.__file_monitor = None
		return

	def __destroy(self):
		self.__unmonitor(self.__uri)
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __monitor(self, uri):
		self.__unmonitor(self.__uri)
		self.__uri = uri
		from gio import File, FILE_MONITOR_NONE
		self.__file_monitor = File(uri).monitor_file(FILE_MONITOR_NONE, None)
		self.__file_monitor.connect("changed", self.__changed_cb)
		return False

	def __unmonitor(self, uri):
		try:
			if not uri or not self.__file_monitor: return False
			self.__file_monitor.cancel()
		except AttributeError:
			pass
		return False

	def __reload(self):
		from URILoader.Manager import Manager
		Manager(self.__editor, self.__editor.uri, self.__editor.encoding)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __monitor_cb(self, editor, uri, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__monitor, uri, priority=PRIORITY_LOW)
		return False

	def __changed_cb(self, *args):
		self.__remove_timer(1)
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(1500, self.__reload, priority=PRIORITY_LOW)
		return False

	def __busy_cb(self, *args):
		self.__unmonitor(self.__uri)
		return False

	def __nobusy_cb(self, *args):
		self.__remove_timer(2)
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer2 = timeout_add(1000, self.__monitor, self.__uri, priority=PRIORITY_LOW)
		return False

	def __saved_file_cb(self, editor, uri, *args):
		self.__uri = uri
		return False

	def __close_cb(self, *args):
		self.__unmonitor(self.__uri)
		self.__remove_timer(1)
		self.__remove_timer(2)
		return False
