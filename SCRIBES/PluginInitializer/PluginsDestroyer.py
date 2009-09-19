class Destroyer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("active-plugins", self.__plugins_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugins = []
		return

	def __destroy(self):
		self.__unload_plugins()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __unload_plugins(self):
		self.__editor.response()
		unload = lambda plugindata: plugindata[-1].unload()
		[unload(plugin) for plugin in self.__plugins]
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __plugins_cb(self, manager, data):
		self.__plugins = data
		return False
