from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "new-scheme", self.__update_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, scheme):
		self.__manager.emit("update-database", scheme.get_id())
		return False

	def __update_timeout(self, scheme):
		from gobject import idle_add
		self.__timer = idle_add(self.__update, scheme, priority=9999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, scheme):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(250, self.__update_timeout, scheme, priority=9999)
		return False
