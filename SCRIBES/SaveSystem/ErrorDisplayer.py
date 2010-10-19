from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "save-failed", self.__failed_cb)
		self.connect(manager, "session-id", self.__session_cb)
		self.connect(manager, "save-succeeded", self.__succeeded_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		self.__error = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __show(self, data):
		session_id, uri, encoding, message = data
		if self.__session_id != tuple(session_id): return False
		if self.__error: return False
		self.__error = True
		self.__editor.show_error(uri, message, busy=True)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False

	def __failed_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__show, data, priority=9999)
		return

	def __succeeded_cb(self, *args):
		self.__error = False
		return False
