class Creator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("create-plugin-path", self.__create_cb)
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

	def __create(self, plugin_path):
		try:
			from os import makedirs, path
			filename = path.join(plugin_path, "__init__.py")
			makedirs(plugin_path)
			handle = open(filename, "w")
			handle.close()
			self.__manager.emit("validate-path", plugin_path)
		except OSError, IOError:
			self.__manager.emit("plugin-folder-creation-error", plugin_path)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __create_cb(self, manager, plugin_path):
		from gobject import idle_add
		idle_add(self.__create, plugin_path)
		return False
