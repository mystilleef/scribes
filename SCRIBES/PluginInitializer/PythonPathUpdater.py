from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "update-python-path", self.__update_cb)
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

	def __update(self, plugin_path):
		self.__editor.response()
		from sys import path
		if not (plugin_path in path): path.insert(0, plugin_path)
		self.__editor.response()
		self.__manager.emit("search-path-updated", plugin_path)
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, plugin_path):
		#from gobject import idle_add
		#idle_add(self.__update, plugin_path)
		self.__update(plugin_path)
		return False
