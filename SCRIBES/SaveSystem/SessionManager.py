class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("save-file", self.__save_cb)
		self.__sigid3 = editor.connect_after("rename-file", self.__save_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__count = 0
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __process(self, uri, encoding):
		try:
			self.__editor.response()
			self.__count += 1
			session_id = self.__editor.id_, self.__count
			self.__manager.emit("session-id", session_id)
			data = uri, encoding, session_id
			if self.__editor.readonly: raise AssertionError
			if self.__editor.generate_filename: raise ValueError
			self.__manager.emit("save-data", data)
		except AssertionError:
			self.__editor.response()
			self.__manager.emit("readonly-error")
		except ValueError:
			self.__editor.response()
			self.__manager.emit("generate-name", data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __save_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__process, uri, encoding)
		return False
