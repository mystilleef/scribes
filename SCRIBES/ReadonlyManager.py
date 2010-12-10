from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		editor.set_data("readonly", False)
		self.connect(editor, "loaded-file", self.__loaded_cb)
		self.connect(editor, "renamed-file", self.__loaded_cb)
		self.connect(editor, "toggle-readonly", self.__toggle_cb)
		self.connect(editor, "quit", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __set(self, readonly):
		self.__editor.set_data("readonly", readonly)
		self.__editor.emit("readonly", readonly)
		return False

	def __check(self, uri):
		self.__set(False) if self.__can_write(uri) else self.__set(True)
		return False

	def __toggle(self):
		try:
			if not self.__can_write(self.__editor.uri): raise ValueError
			self.__set(False) if self.__editor.readonly else self.__set(True)
		except ValueError:
			print "Error: You do not have permission to write to the file."
		return False

	def __can_write(self, uri):
		from Utils import check_uri_permission #FIXME: Bad function name
		return check_uri_permission(uri)

	def __loaded_cb(self, editor, uri, encoding):
		self.__check(uri)
		return False

	def __toggle_cb(self, *args):
		self.__toggle()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
