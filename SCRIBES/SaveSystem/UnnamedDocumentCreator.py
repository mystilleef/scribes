class Creator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("create-new-file", self.__create_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __create(self, _data):
		uri, data = _data
		self.__editor.create_uri(uri)
		data = uri, data[1], data[2]
		self.__manager.emit("save-data", data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __create_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__create, data, priority=9999)
		return False