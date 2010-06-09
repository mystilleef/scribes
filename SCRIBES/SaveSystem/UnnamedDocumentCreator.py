from SCRIBES.SignalConnectionManager import SignalManager

class Creator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "create-new-file", self.__create_cb)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__count = 0
		return

	def __destroy(self):
		self.__editor.response()
		if self.__count: return True
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __create(self, _data):
		self.__count += 1
		from gio import File
		uri, data = _data
		File(uri).create_async(self.__create_async_cb, user_data=_data)
		return False

	def __optimize(self):
		self.__editor.optimize((self.__create,))
		return False

	def __create_async_cb(self, gfile, result, _data):
		outputstream = gfile.create_finish(result)
		outputstream.close_async(self.__close_async_cb, user_data=_data)
		return False

	def __close_async_cb(self, gfile, result, _data):
		succeeded = gfile.close_finish(result)
		uri, data = _data
		data = uri, data[1], data[2]
		self.__manager.emit("save-data", data)
		self.__count -= 1
		return False

	def __quit_cb(self, *args):
		from gobject import timeout_add
		timeout_add(50, self.__destroy, priority=9999)
		return False

	def __create_cb(self, manager, data):
		self.__editor.response()
		from gobject import idle_add
		idle_add(self.__create, data, priority=9999)
		return False
