from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		from gobject import timeout_add, PRIORITY_LOW as LOW
		timeout_add(1000, self.__validate_timeout, priority=LOW)
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

	def __emit(self, plugin_path):
		self.__editor.refresh(False)
		self.__manager.emit("validate-path", plugin_path)
		self.__editor.refresh(False)
		return

	def __validate(self):
		self.__editor.refresh(False)
		[self.__emit(plugin_path) for plugin_path in self.__plugin_paths]
		self.__editor.refresh(False)
		return False

	def __validate_timeout(self):
		from gobject import idle_add, PRIORITY_LOW as LOW
		idle_add(self.__validate, priority=LOW)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
