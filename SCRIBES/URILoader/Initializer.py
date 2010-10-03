from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor, uri, encoding):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attibutes(manager, editor)
		self.connect(editor, "load-file", self.__load_file_cb)
		self.connect(manager, "destroy", self.__destroy_cb)
		if uri: editor.load_file(uri, encoding)
		editor.response()

	def __init_attibutes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __load(self, uri, encoding):
		self.__manager.emit("init-loading", uri, encoding)
		self.__manager.emit("check-file-type", uri)
		return False

	def __load_timeout(self, uri, encoding):
		from gobject import idle_add
		idle_add(self.__load, uri, encoding)
		return False

	def __load_file_cb(self, editor, uri, encoding):
		from gobject import timeout_add
		timeout_add(25, self.__load_timeout, uri, encoding)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
