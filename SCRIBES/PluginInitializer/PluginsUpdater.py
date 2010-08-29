from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroyed-plugins", self.__quit_cb)
		self.connect(manager, "loaded-plugin", self.__loaded_cb)
		self.connect(manager, "unloaded-plugin", self.__unloaded_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugins = []
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self, data, remove=False):
		self.__editor.response()
		self.__plugins.remove(data) if remove else self.__plugins.append(data)
		self.__editor.response()
		self.__manager.emit("active-plugins", self.__plugins)
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __loaded_cb(self, manager, data):
		self.__update(data)
		return False

	def __unloaded_cb(self, manager, data):
		self.__update(data, True)
		return False
