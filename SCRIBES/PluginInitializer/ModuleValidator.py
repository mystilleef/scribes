from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "initialized-module", self.__validate_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __validate(self, module):
		try:
			from gobject import idle_add
			emit = lambda signal: idle_add(self.__manager.emit, signal, module)
			if not hasattr(module, "autoload"): raise ValueError
			if not hasattr(module, "name"): raise ValueError
			if not hasattr(module, "version"): raise ValueError
			if not hasattr(module, "class_name"): raise ValueError
			emit("validate-language-module") if hasattr(module, "languages") else emit("valid-module")
		except ValueError:
			print module, " is an invalid plugin module"
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __validate_cb(self, manager, module):
		from gobject import idle_add
		idle_add(self.__validate, module)
		return False
