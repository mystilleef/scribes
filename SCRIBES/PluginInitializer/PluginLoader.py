from SCRIBES.SignalConnectionManager import SignalManager

class Loader(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "load-plugin", self.__load_cb)
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

	def __load(self, data):
		self.__editor.response()
		module, PluginClass = data
		if module.autoload is False: return False
		self.__editor.response()
		plugin = PluginClass(self.__editor)
		self.__editor.response()
		plugin.load()
		self.__editor.response()
		self.__manager.emit("loaded-plugin", (module, plugin))
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __load_cb(self, manager, data):
		self.__load(data)
		return False
