class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("update", self.__update_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, image_id, time):
		try:
			self.__manager.emit("busy", True)
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__manager.emit("update-image", image_id)
			self.__timer = timeout_add(time * 1000, self.__reset, priority=9999)
		return False

	def __reset(self):
		self.__manager.emit("busy", False)
		self.__manager.emit("reset")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False 

	def __update_cb(self, manager, image_id, time):
		from gobject import idle_add
		idle_add(self.__update, image_id, time, priority=9999)
		return False
