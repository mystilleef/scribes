class Unloader(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("unload-plugin", self.__unload_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __unload(self, data):
		module, plugin = data
		self.__editor.response()
		plugin.unload()
		self.__editor.response()
		self.__manager.emit("unloaded-plugin", (module, plugin))
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __unload_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__unload, data)
		return False