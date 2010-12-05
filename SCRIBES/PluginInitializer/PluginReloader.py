from SCRIBES.SignalConnectionManager import SignalManager

class Reloader(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "active-plugins", self.__plugins_cb)
		self.connect(editor, "loaded-file", self.__loaded_cb, True)
		self.connect(editor, "renamed-file", self.__loaded_cb, True)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugins = []
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __load_language_plugins(self):
		is_language_plugin = lambda data: hasattr(data[0], "languages")
		unload = lambda plugin: self.__manager.emit("unload-plugin", plugin)
		from copy import copy
		[unload(plugin) for plugin in copy(self.__plugins) if is_language_plugin(plugin)]
		paths = (self.__editor.core_language_plugin_folder, self.__editor.home_language_plugin_folder,)
		load = lambda path: self.__manager.emit("search-path-updated", path)
		[load(path) for path in paths]
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __plugins_cb(self, manager, data):
		self.__plugins = data
		return False

	def __loaded_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_language_plugins)
#		self.__load_language_plugins()
		return False
