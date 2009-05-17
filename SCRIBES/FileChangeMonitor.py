#FIXME: Clean up this module. Too many poorly named variables.

class Monitor(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect_after("loaded-file", self.__monitor_cb)
		self.__sigid3 = editor.connect_after("renamed-file", self.__monitor_cb)
		self.__sigid4 = editor.connect("save-file", self.__busy_cb)
		self.__sigid5 = editor.connect_after("save-error", self.__nobusy_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__uri = ""
		self.__monitoring = False
		self.__busy = False
		self.__block = False
		return

	def __destroy(self):
		self.__unmonitor(self.__uri)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __monitor(self, uri):
		self.__unmonitor(self.__uri)
		if uri.startswith("file:///") is False: return False
		self.__uri = uri
		from gio import File, FILE_MONITOR_NONE
		self.__file_monitor = File(uri).monitor_file(FILE_MONITOR_NONE, None)
		self.__file_monitor.connect("changed", self.__changed_cb)
		self.__monitoring = True
		return False

	def __unmonitor(self, uri):
		if not uri: return False
		if self.__monitoring is False: return False
		self.__file_monitor.cancel()
		self.__monitoring = False
		return False

	def __process(self, args):
		try:
			monitor, gfile, otherfile, event = args
			if not (event in (0, 3)): return False
			if self.__block: return False
			self.__block = True
			from gobject import timeout_add, idle_add
			timeout_add(500, self.__unblock)
			if self.__busy: raise ValueError
			idle_add(self.__reload)
		except ValueError:
			self.__busy = False
		return False

	def __reload(self):
		from URILoader.Manager import Manager
		Manager(self.__editor, self.__editor.uri, self.__editor.encoding)
		return False

	def __unblock(self):
		self.__block = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __monitor_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__monitor, uri, priority=9999)
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__process, args, priority=9999)
		return False

	def __busy_cb(self, *args):
		self.__busy = True
		return False

	def __nobusy_cb(self, *args):
		self.__busy = False
		return False
