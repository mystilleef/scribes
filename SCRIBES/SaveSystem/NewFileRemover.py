class Remover(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__destroy_cb)
		self.__sigid2 = manager.connect("create-new-file", self.__create_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__renamed_cb)
		self.__sigid4 = manager.connect("remove-new-file", self.__remove_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__uri = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
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
		idle_add(self.__create, data)
		return False

	def __renamed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__remove)
		return False

	def __remove_cb(self, *args):
		self.__remove()
		return False
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False
