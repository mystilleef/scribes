from SCRIBES.SignalConnectionManager import SignalManager

class Emitter(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "rename-file", self.__rename_cb)
		self.connect(manager, "session-id", self.__session_cb)
		self.connect(manager, "saved", self.__saved_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__rename = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __emit(self, data):
		session_id, uri, encoding = data
		if tuple(session_id) != self.__session_id: return False
		self.__editor.emit("saved-file", uri, encoding)
		if not self.__rename: return False
		self.__editor.emit("renamed-file", uri, encoding)
		self.__rename = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False

	def __saved_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__emit, data, priority=9999)
		return False

	def __rename_cb(self, *args):
		self.__rename = True
		return False
