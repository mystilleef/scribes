class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("modified-file", self.__modified_cb)
		self.__sigid3 = manager.connect("busy", self.__busy_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self):
		if self.__busy: return False
		self.__manager.emit("reset")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False

	def __modified_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False
