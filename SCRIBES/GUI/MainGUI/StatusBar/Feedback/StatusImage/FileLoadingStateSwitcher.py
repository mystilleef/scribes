class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__checking_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__loaded_cb)
		self.__sigid4 = editor.connect("load-error", self.__error_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self):
		self.__manager.emit("update", "gtk-open", 3)
		self.__manager.emit("unset", "busy")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, *args):
		self.__manager.emit("set", "busy")
		return False

	def __loaded_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False

	def __error_cb(self, *args):
		self.__manager.emit("unset", "busy")
		return False
