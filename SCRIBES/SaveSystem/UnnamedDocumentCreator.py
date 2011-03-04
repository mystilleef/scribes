from SCRIBES.SignalConnectionManager import SignalManager

class Creator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "create-new-file", self.__create_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__optimize, priority=PRIORITY_LOW)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__count = 0
		return

	def __create(self, _data):
		self.__count += 1
		from gio import File
		uri, data = _data
		File(uri).create_async(self.__create_async_cb, user_data=_data)
		return False

	def __create_on_idle(self, _data):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__create, _data, priority=PRIORITY_LOW)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __optimize(self):
		self.__editor.optimize((self.__create,))
		return False

	def __destroy(self):
		if self.__count: return True
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __create_async_cb(self, gfile, result, _data):
		outputstream = gfile.create_finish(result)
		outputstream.close_async(self.__close_async_cb, user_data=_data)
		return False

	def __close_async_cb(self, gfile, result, _data):
		gfile.close_finish(result)
		uri, data = _data
		from gobject import idle_add
		idle_add(self.__manager.emit, "created-new-file", uri)
		data = uri, data[1], data[2]
		idle_add(self.__manager.emit, "save-data", data)
		self.__count -= 1
		return False

	def __quit_cb(self, *args):
		from gobject import timeout_add, PRIORITY_LOW
		timeout_add(250, self.__destroy, priority=PRIORITY_LOW)
		return False

	def __create_cb(self, manager, data):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer2 = timeout_add(250, self.__create_on_idle, data, priority=PRIORITY_LOW)
		return False
