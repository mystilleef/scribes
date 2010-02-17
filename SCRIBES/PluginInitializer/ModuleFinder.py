class Finder(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("search-path-updated", self.__find_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __initialize_modules(self, plugin_path):
		_path = plugin_path.strip("/")
		if not self.__editor.language and _path.endswith("LanguagePlugins"): return False
		is_plugin = lambda filename: filename.startswith("Plugin") and filename.endswith(".py")
		from os import listdir, path
		fullpath = lambda filename: path.join(plugin_path, filename)
		modules = [fullpath(filename) for filename in listdir(plugin_path) if is_plugin(filename)]
		initialize = lambda module: self.__manager.emit("initialize-module", module)
		[initialize(module) for module in modules]
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __find_cb(self, manager, plugin_path):
		from gobject import idle_add
		idle_add(self.__initialize_modules, plugin_path)
		return False
