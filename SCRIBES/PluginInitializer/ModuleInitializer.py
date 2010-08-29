from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "initialize-module", self.__initialize_cb)
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

	def __initialize(self, module_path):
		self.__editor.response()
		from os.path import split
		module_name = split(module_path)[-1][:-3]
		from imp import load_source
		self.__editor.response()
		module = load_source(module_name, module_path)
		self.__editor.response()
		self.__manager.emit("initialized-module", module)
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __initialize_cb(self, manager, module_path):
		#from gobject import idle_add
		#idle_add(self.__initialize, module_path)
		self.__initialize(module_path)
		return False
