from SCRIBES.SignalConnectionManager import SignalManager

class Detector(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "active-plugins", self.__plugins_cb)
		self.connect(manager, "check-duplicate-plugins", self.__check_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Successfully loaded plugin modules.
		self.__modules = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __handle_duplicate(self, unloaded_plugin_data, loaded_plugin_data):
		self.__editor.response()
		unloaded_module = unloaded_plugin_data[0]
		loaded_module = loaded_plugin_data[0]
		if loaded_module.version >= unloaded_module.version: return False
		print "Loading new duplicate plugin"
		print loaded_module.class_name, loaded_module.version, unloaded_module.class_name, unloaded_module.version
		self.__manager.emit("unload-plugin", loaded_plugin_data)
		self.__manager.emit("load-plugin", unloaded_plugin_data)
		self.__editor.response()
		return False

	def __get_duplicate(self, unloaded_plugin_data):
		self.__editor.response()
		if not self.__modules: return None
		module, plugin_class = unloaded_plugin_data
		from copy import copy
		for _module, _plugin in copy(self.__modules):
			self.__editor.response()
			if module.class_name == _module.class_name: return (_module, _plugin)
		self.__editor.response()
		return None

	def __check(self, unloaded_plugin_data):
		self.__editor.response()
		loaded_plugin_data = self.__get_duplicate(unloaded_plugin_data)
		self.__handle_duplicate(unloaded_plugin_data, loaded_plugin_data) if loaded_plugin_data else self.__manager.emit("load-plugin", unloaded_plugin_data)
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __plugins_cb(self, manager, plugins):
		self.__modules = plugins
		return False

	def __check_cb(self, manager, unloaded_plugin_data):
		self.__check(unloaded_plugin_data)
		return False
