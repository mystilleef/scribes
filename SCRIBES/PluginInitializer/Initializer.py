class Initializer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		from gobject import idle_add
		idle_add(self.__validate)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugin_paths = (
			editor.core_plugin_folder,
			editor.home_plugin_folder,
			editor.core_language_plugin_folder,
			editor.home_language_plugin_folder,
		)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __validate(self):
		validate = lambda plugin_path: self.__manager.emit("validate-path", plugin_path)
		[validate(plugin_path) for plugin_path in self.__plugin_paths]
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
