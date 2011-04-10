from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor, uri, encoding):
		SignalManager.__init__(self, editor)
		self.__init_attibutes(manager, editor)
		self.connect(editor, "load-file", self.__load_file_cb)
		self.connect(manager, "destroy", self.__destroy_cb)
		if uri: editor.load_file(uri, encoding)

	def __init_attibutes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __load(self, uri, encoding):
		from gobject import idle_add, PRIORITY_HIGH, PRIORITY_LOW
		idle_add(self.__manager.emit, "init-loading", uri, encoding, priority=PRIORITY_HIGH)
		idle_add(self.__manager.emit, "check-file-type", uri, priority=PRIORITY_LOW)
		return False

	def __load_file_cb(self, editor, uri, encoding):
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__load, uri, encoding, priority=PRIORITY_HIGH)
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
