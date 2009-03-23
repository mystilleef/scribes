class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("set", self.__set_cb)
		self.__sigid3 = manager.connect("unset", self.__unset_cb)
		self.__sigid4 = manager.connect("reset", self.__reset_cb)
		self.__sigid5 = manager.connect("busy", self.__busy_cb)
		editor.register_object(self)
		editor.response()

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

	def __set(self, image_id):
		self.__queue.append(image_id)
		if self.__busy: return False
		self.__reset()
		return False

	def __unset(self, image_id):
		try:
			self.__queue.remove(image_id)
			if self.__busy: return False
			self.__reset()
		except ValueError:
			pass
		return False

	def __reset(self):
		try:
			if self.__busy: return False
			self.__manager.emit("update-image", self.__queue[-1])
		except IndexError:
			self.__manager.emit("fallback")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __set_cb(self, manager, image_id):
		from gobject import idle_add
		idle_add(self.__set, image_id, priority=9999)
		return False

	def __unset_cb(self, manager, image_id):
		from gobject import idle_add
		idle_add(self.__unset, image_id, priority=9999)
		return False

	def __reset_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__reset, priority=9999)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False
