from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "initialized-module", self.__validate_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __emit(self, signal, module):
		self.__editor.response()
		self.__manager.emit(signal, module)
		self.__editor.response()
		return False

	def __validate(self, module):
		try:
			self.__editor.response()
			if not hasattr(module, "autoload"): raise ValueError
			if not hasattr(module, "name"): raise ValueError
			if not hasattr(module, "version"): raise ValueError
			if not hasattr(module, "class_name"): raise ValueError
			self.__emit("validate-language-module", module) if hasattr(module, "languages") else self.__emit("valid-module", module)
		except ValueError:
			print module, " is an invalid plugin module"
		finally:
			self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __validate_cb(self, manager, module):
		self.__validate(module)
		return False
