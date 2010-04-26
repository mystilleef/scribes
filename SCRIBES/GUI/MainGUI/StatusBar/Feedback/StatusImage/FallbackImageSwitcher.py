class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("fallback", self.__fallback_cb)
		self.__sigid3 = manager.connect("busy", self.__busy_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __fallback(self):
		try:
			if self.__busy: return False
			emit = lambda image_id: self.__manager.emit("update-image", image_id)
			if not self.__editor.uri: raise ValueError
			emit("edit") if self.__editor.modified else emit("new")
		except ValueError:
			emit("")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fallback_cb(self, *args):
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(300, self.__fallback, priority=99999)
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False
