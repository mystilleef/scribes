from SCRIBES.SignalConnectionManager import SignalManager

class Remover(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(editor, "renamed-file", self.__check_cb)
		self.connect(manager, "created-new-file", self.__check_cb)
		self.connect(manager, "remove-new-file", self.__remove_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__uri = ""
		self.__quit = False
		return

	def __check(self, uri):
		if self.__uri == uri: return False
		self.__remove(self.__uri)
		self.__uri = uri
		if self.__quit: self.__destroy()
		return False

	def __remove(self, uri):
		if not uri: return False
		if self.__editor.uri_exists(uri) is False: return False
		self.__editor.remove_uri(uri)
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __check_cb(self, editor, uri):
		from gobject import idle_add
		idle_add(self.__check, uri)
		return False

	def __remove_cb(self, *args):
		self.__quit = True
		self.__remove(self.__uri)
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __destroy_cb(self, *args):
		if self.__quit: return False
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
