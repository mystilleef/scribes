from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		from gobject import timeout_add, PRIORITY_HIGH as HIGH
		timeout_add(50, self.__validate_timeout, priority=HIGH)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugin_paths = (
			editor.home_plugin_folder,
			editor.core_plugin_folder,
			editor.home_language_plugin_folder,
			editor.core_language_plugin_folder,
		)
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __validate(self):
		from gobject import idle_add
		emit = self.__manager.emit
		[idle_add(emit, "validate-path", plugin_path) for plugin_path in self.__plugin_paths]
		return False

	def __validate_timeout(self):
		from gobject import idle_add, PRIORITY_HIGH as HIGH
		idle_add(self.__validate, priority=HIGH)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
