from SCRIBES.SignalConnectionManager import SignalManager

RATE_LIMIT = 25 # in milliseconds

class Monitor(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.__file_monitor.set_rate_limit(RATE_LIMIT)
		self.__file_monitor.cancel()
		self.connect(editor, "close", self.__close_cb)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "saved-file", self.__saved_file_cb)
		self.connect(editor, "save-file", self.__busy_cb)
		self.connect(editor, "save-error", self.__nobusy_cb, True)
		self.connect(editor, "saved-file", self.__nobusy_cb, True)
		self.connect(editor, "loaded-file", self.__monitor_cb, True)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__uri = ""
		from gio import File, FILE_MONITOR_NONE
		self.__file_monitor = File("").monitor_file(FILE_MONITOR_NONE, None)
		self.__timer1, self.__timer2 = "", ""
		self.__is_monitoring = False
		return

	def __monitor(self, uri):
		self.__unmonitor()
		self.__uri = uri
		from gio import File, FILE_MONITOR_NONE
		self.__file_monitor = File(uri).monitor_file(FILE_MONITOR_NONE, None)
		self.__file_monitor.connect("changed", self.__changed_cb)
		self.__file_monitor.set_rate_limit(RATE_LIMIT)
		self.__is_monitoring = True
		return False

	def __unmonitor(self):
		if self.__is_monitoring is False: return False
		self.__file_monitor.cancel()
		self.__is_monitoring = False
		return False

	def __reload(self):
		if self.__file_exists() is False: return False
		from URILoader.Manager import Manager
		Manager(self.__editor, self.__editor.uri, self.__editor.encoding)
		from gobject import timeout_add, PRIORITY_LOW
		timeout_add(3000, self.__reload_feedback_message, priority=PRIORITY_LOW)
		return False

	def __reload_feedback_message(self):
		from gettext import gettext as _
		message = _("File modification detected. Reloaded file")
		self.__editor.update_message(message, "info", 10)
		return False

	def __file_exists(self):
		from gio import File
		return File(self.__uri).query_exists()

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except TypeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __monitor_cb(self, editor, uri, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__monitor, uri, priority=PRIORITY_LOW)
		return False

	def __changed_cb(self, monitor, child, other_child, event):
		if event not in (1, 3): return False
		self.__remove_all_timers()
		self.__unmonitor()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(1500, self.__reload, priority=PRIORITY_LOW)
		return False

	def __busy_cb(self, *args):
		self.__remove_all_timers()
		self.__unmonitor()
		return False

	def __nobusy_cb(self, *args):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer2 = timeout_add(1000, self.__monitor, self.__uri, priority=PRIORITY_LOW)
		return False

	def __saved_file_cb(self, editor, uri, *args):
		self.__uri = uri
		return False

	def __close_cb(self, *args):
		self.__remove_all_timers()
		self.__unmonitor()
		return False
