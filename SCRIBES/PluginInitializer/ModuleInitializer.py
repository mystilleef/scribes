class Initializer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("initialize-module", self.__initialize_cb)
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

	def __initialize(self, module_path):
		from os.path import split
		module_name = split(module_path)[-1][:-3]
		from imp import load_source
		self.__editor.response()
		module = load_source(module_name, module_path)
		self.__editor.response()
		self.__manager.emit("initialized-module", module)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __initialize_cb(self, manager, module_path):
		from gobject import idle_add
		idle_add(self.__initialize, module_path)
		return False
