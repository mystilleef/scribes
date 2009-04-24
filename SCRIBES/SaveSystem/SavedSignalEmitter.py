class Emitter(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("rename-file", self.__rename_cb)
		self.__sigid3 = manager.connect("session-id", self.__session_cb)
		self.__sigid4 = manager.connect("saved", self.__saved_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__rename = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit(self, data):
		session_id, uri, encoding = data
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
