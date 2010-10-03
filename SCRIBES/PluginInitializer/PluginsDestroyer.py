from SCRIBES.SignalConnectionManager import SignalManager

class Destroyer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "active-plugins", self.__plugins_cb, True)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__quit = False
		self.__plugins = []
		self.__destroyed = False
		return

	def __destroy(self):
		self.disconnect()
		self.__manager.emit("destroyed-plugins")
		self.__editor.unregister_object(self)
		del self
		return False

	def __check(self):
		self.__editor.response()
		if self.__destroyed: return False
		if self.__quit is False: return False
		if self.__plugins: return False
		from gobject import idle_add
		idle_add(self.__destroy)
		self.__destroyed = True
		return False

	def __unload(self, plugin_data):
		self.__editor.response()
		self.__manager.emit("unload-plugin", plugin_data)
		self.__editor.response()
		return

	def __unload_plugins(self):
		from copy import copy
		self.__editor.response()
		[self.__unload(plugin_data) for plugin_data in copy(self.__plugins)]
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		try:
			if not self.__plugins: raise ValueError
			self.__quit = True
			from gobject import idle_add
			idle_add(self.__unload_plugins)
		except ValueError:
			self.__destroy()
		return False

	def __plugins_cb(self, manager, plugins):
		self.__plugins = plugins
		from gobject import idle_add
		idle_add(self.__check)
		return False
