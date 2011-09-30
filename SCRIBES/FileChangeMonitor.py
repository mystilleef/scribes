from SCRIBES.SignalConnectionManager import SignalManager

RATE_LIMIT = 100 # in milliseconds
WAIT_INTERVAL = 1500 # in milliseconds
IGNORE_MONITORING_INTERVAL = WAIT_INTERVAL * 3

class Monitor(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
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
		from gio import File, FILE_MONITOR_NONE, Cancellable
		self.__cancellable = Cancellable()
		self.__file_monitor = File("").monitor_file(FILE_MONITOR_NONE, self.__cancellable)
		self.__timer1, self.__timer2 = "", ""
		self.__can_reload = True
		return

	def __monitor(self, uri):
		self.__uri = uri
		from gio import File, FILE_MONITOR_NONE
		self.__unmonitor()
		self.__file_monitor = File(uri).monitor_file(FILE_MONITOR_NONE, self.__cancellable)
		self.__file_monitor.connect("changed", self.__changed_cb)
		self.__file_monitor.set_rate_limit(RATE_LIMIT)
		return False

	def __unmonitor(self):
		self.__file_monitor.cancel()
		self.__cancellable.cancel()
		self.__cancellable.reset()
		return False

	def __remove_monitor(self):
		self.__remove_all_timers()
		self.__unmonitor()
		return False

	def __set_can_reload(self, can_reload):
		self.__can_reload = can_reload
		return False

	def __reload(self):
		if self.__file_exists() is False: return False
		from URILoader.Manager import Manager
		Manager(self.__editor, self.__uri, self.__editor.encoding)
		from gobject import timeout_add, PRIORITY_LOW
		timeout_add(1000, self.__reload_feedback_message, priority=PRIORITY_LOW)
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

	def __change_handler(self, event):
		if self.__can_reload is False or event not in (1, 3): return False
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__reload, priority=PRIORITY_LOW)
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
		self.__remove_all_timers()
		from gobject import timeout_add
		self.__timer1 = timeout_add(WAIT_INTERVAL, self.__change_handler, event)
		return False

	def __busy_cb(self, *args):
		self.__can_reload = False
		self.__remove_all_timers()
		return False

	def __nobusy_cb(self, *args):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer2 = timeout_add(IGNORE_MONITORING_INTERVAL, self.__set_can_reload, True, priority=PRIORITY_LOW)
		return False

	def __saved_file_cb(self, editor, uri, *args):
		if self.__uri == uri: return False
		self.__monitor(uri)
		return False

	def __close_cb(self, *args):
		self.__remove_monitor()
		return False
