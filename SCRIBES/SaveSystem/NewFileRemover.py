from SCRIBES.SignalConnectionManager import SignalManager

class Remover(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(manager, "create-new-file", self.__create_cb)
		self.connect(editor, "renamed-file", self.__renamed_cb)
		self.connect(manager, "remove-new-file", self.__remove_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__uri = ""
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __remove(self):
		if self.__uri: self.__editor.remove_uri(self.__uri)
		return False

	def __create(self, _data):
		uri, data = _data
		self.__remove()
		self.__uri = uri
		return False

	def __create_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__create, data, priority=9999)
		return False

	def __renamed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__remove, priority=9999)
		return False

	def __remove_cb(self, *args):
		self.__remove()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
