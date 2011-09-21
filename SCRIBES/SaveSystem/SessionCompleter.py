from SCRIBES.SignalConnectionManager import SignalManager

class Completer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "save-succeeded", self.__data_cb)
		self.connect(manager, "save-failed", self.__data_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __verify_session(self, data):
		from gobject import idle_add
		emit = lambda signal: idle_add(self.__manager.emit, signal, data)
		emit("saved?") if len(data) == 3 else emit("error")
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__verify_session, data)
		return False
