class Validator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("validate-path", self.__validate_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
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
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __validate_cb(self, manager, plugin_path):
		from gobject import idle_add
		idle_add(self.__validate, plugin_path)
		return False
