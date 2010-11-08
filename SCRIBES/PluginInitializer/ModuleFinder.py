from SCRIBES.SignalConnectionManager import SignalManager

class Finder(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "search-path-updated", self.__find_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __is_plugin(self, filename):
		self.__editor.refresh(False)
		return filename.startswith("Plugin") and filename.endswith(".py")

	def __fullpath(self, plugin_path, filename):
		from os import path
		self.__editor.refresh(False)
		return path.join(plugin_path, filename)

	def __initialize(self, module):
		self.__editor.refresh(False)
		self.__manager.emit("initialize-module", module)
		self.__editor.refresh(False)
		return

	def __initialize_modules(self, plugin_path):
		self.__editor.refresh(False)
		_path = plugin_path.strip("/")
		if not self.__editor.language and _path.endswith("LanguagePlugins"): return False
		from os import listdir
		self.__editor.refresh(False)
		modules = [self.__fullpath(plugin_path, filename) for filename in listdir(plugin_path) if self.__is_plugin(filename)]
		self.__editor.refresh(False)
		[self.__initialize(module) for module in modules]
		self.__editor.refresh(False)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __find_cb(self, manager, plugin_path):
		self.__initialize_modules(plugin_path)
		return False
