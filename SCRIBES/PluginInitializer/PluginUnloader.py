from SCRIBES.SignalConnectionManager import SignalManager

class Unloader(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroyed-plugins", self.__quit_cb)
		self.connect(manager, "unload-plugin", self.__unload_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __unload(self, data):
		module, plugin = data
		self.__editor.response()
		plugin.unload()
		self.__editor.response()
		self.__manager.emit("unloaded-plugin", (module, plugin))
#		print "Unloaded: ", plugin
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __unload_cb(self, manager, data):
		self.__unload(data)
		return False
