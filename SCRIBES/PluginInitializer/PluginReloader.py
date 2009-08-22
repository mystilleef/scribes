class Reloader(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("active-plugins", self.__plugins_cb)
		self.__sigid3 = editor.connect_after("loaded-file", self.__loaded_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugins = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __load_language_plugins(self):
		is_language_plugin = lambda data: hasattr(data[0], "languages")
		unload = lambda plugin: self.__manager.emit("unload-plugin", plugin)
		[unload(plugin) for plugin in self.__plugins if is_language_plugin(plugin)]
		paths = (self.__editor.core_language_plugin_folder, self.__editor.home_language_plugin_folder,)
		load = lambda path: self.__manager.emit("search-path-updated", path)
		[load(path) for path in paths]
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __plugins_cb(self, manager, data):
		self.__plugins = data
		return False

	def __loaded_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_language_plugins)
		return False
