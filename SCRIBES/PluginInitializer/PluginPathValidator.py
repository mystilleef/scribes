from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "validate-path", self.__validate_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __validate(self, plugin_path):
		try:
			self.__editor.response()
			from os.path import join, exists
			filename = join(plugin_path, "__init__.py")
			if not exists(filename): raise ValueError
			self.__manager.emit("update-python-path", plugin_path)
		except ValueError:
			self.__manager.emit("plugin-path-error", plugin_path)
		finally:
			self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __validate_cb(self, manager, plugin_path):
		self.__validate(plugin_path)
		return False
