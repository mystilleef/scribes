class Validator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("session-id", self.__session_cb)
		self.__sigid3 = manager.connect("validate-save-data", self.__validate_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __validate(self, data):
		try:
			if self.__editor.readonly: raise AssertionError
			uri, encoding, session_id = data
			uri = uri if uri else self.__editor.uri
			if not uri: raise ValueError
			if not encoding: encoding = "utf-8"
			data = session_id, uri, encoding
			if session_id != self.__session_id: return False
			self.__manager.emit("save-data", data)
		except ValueError:
			self.__manager.emit("show-save-dialog")
		except AssertionError:
			self.__manager.emit("readonly-error")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __validate_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__validate, data, priority=9999)
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False
