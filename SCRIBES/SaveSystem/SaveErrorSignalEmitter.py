from SCRIBES.SignalConnectionManager import SignalManager

class Emitter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "error", self.__failed_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __emit(self, data):
		session_id, uri, encoding, message = data
		from gobject import idle_add
		idle_add(self.__editor.emit, "save-error", uri, encoding, message)
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

	def __failed_cb(self, manager, data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__emit, data, priority=PRIORITY_LOW)
		return False
