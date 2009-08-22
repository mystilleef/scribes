class Validator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("valid-module", self.__validate_cb)
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

	def __validate(self, module):
		try:
			class_name = getattr(module, "class_name")
			if not hasattr(module, class_name): raise ValueError
			PluginClass = getattr(module, class_name)
			if hasattr(PluginClass, "__init__") is False: raise ValueError
			if hasattr(PluginClass, "load") is False: raise ValueError
			if hasattr(PluginClass, "unload") is False: raise ValueError
			self.__manager.emit("initialize-plugin", (module, PluginClass))
		except ValueError:
			print module, " has an invalid plugin class"
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __validate_cb(self, manager, module):
		from gobject import idle_add
		idle_add(self.__validate, module)
		return False
