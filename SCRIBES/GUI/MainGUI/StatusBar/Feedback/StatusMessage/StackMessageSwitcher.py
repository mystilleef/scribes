class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("set", self.__set_cb)
		self.__sigid3 = manager.connect("unset", self.__unset_cb)
		self.__sigid4 = manager.connect("reset", self.__reset_cb)
		self.__sigid5 = manager.connect("busy", self.__busy_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__queue = []
		self.__busy = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self, message):
		self.__queue.append(message)
		self.__reset()
		return False

	def __unset(self, message):
		try:
			self.__queue.remove(message)
		except ValueError:
			pass
		finally:
			self.__reset()
		return False

	def __reset(self):
		try:
			if self.__busy: return False
			if not self.__queue: raise ValueError
			self.__manager.emit("update-message", self.__queue[-1], True, False, "brown")
		except ValueError:
			self.__manager.emit("fallback")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __set_cb(self, manager, message):
		from gobject import idle_add
		idle_add(self.__set, message, priority=9999)
		return False

	def __unset_cb(self, manager, message):
		from gobject import idle_add
		idle_add(self.__unset, message, priority=9999)
		return False

	def __reset_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__reset, priority=9999)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False
