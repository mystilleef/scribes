from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, editor, uri):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(editor, "loaded-file", self.__loaded_cb, True)
		self.connect(editor, "load-error", self.__loaded_cb)
		if not uri: self.__init_plugins()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __init_plugins(self):
		from PluginInitializer.Manager import Manager
		Manager(self.__editor)
		self.__editor.emit("ready")
		self.__editor.textview.grab_focus()
		self.__destroy()
		return False

	def __loaded_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__init_plugins, priority=PRIORITY_LOW)
		return False
