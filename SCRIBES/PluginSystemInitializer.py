from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, editor, uri):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(editor, "loaded-file", self.__loaded_cb)
		self.connect(editor, "loaded-file", self.__loaded_after_cb, True)
		self.connect(editor, "load-error", self.__loaded_cb)
		self.connect(editor, "load-error", self.__loaded_after_cb, True)
		if not uri: self.__ready()
		if not uri: self.__init_plugins()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __init_plugins(self):
		from PluginInitializer.Manager import Manager
		Manager(self.__editor)
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __ready(self):
		self.__editor.emit("ready")
		self.__editor.refresh(True)
		return False

	def __init_plugins_on_idle(self):
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__init_plugins, priority=PRIORITY_HIGH)
		return False

	def __loaded_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__ready)
		return False

	def __loaded_after_cb(self, *args):
		from gobject import timeout_add, PRIORITY_HIGH
		timeout_add(50, self.__init_plugins_on_idle, priority=PRIORITY_HIGH)
		return False
