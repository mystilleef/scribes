from SCRIBES.SignalConnectionManager import SignalManager

class Unloader(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "post-quit", self.__quit_cb)
		self.connect(manager, "unload-plugin", self.__unload_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __unload(self, data):
		module, plugin = data
		plugin.unload()
		emit = self.__manager.emit
		from gobject import idle_add
		idle_add(emit, "unloaded-plugin", (module, plugin))
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __unload_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__unload, data)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
