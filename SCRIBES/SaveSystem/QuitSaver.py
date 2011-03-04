from SCRIBES.SignalConnectionManager import SignalManager

class Saver(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "close", self.__close_cb)
		self.connect(manager, "save-succeeded", self.__saved_cb)
		self.connect(manager, "save-failed", self.__error_cb)
		self.connect(manager, "session-id", self.__session_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		self.__quit = False
		self.__error = False
		return

	def __save(self):
		self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		return False

	def __close(self, save_file):
		try:
			if save_file is False: raise StandardError
			if self.__error: raise ValueError
			if self.__editor.modified is False: raise ValueError
			self.__quit = True
			from gobject import idle_add, PRIORITY_LOW
			idle_add(self.__save, priority=PRIORITY_LOW)
		except ValueError:
			self.__destroy()
		except StandardError:
			self.__manager.emit("remove-new-file")
			self.__destroy()
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		self.__editor.emit("quit")
		del self
		return False

	def __close_cb(self, editor, save_file):
		from gobject import idle_add
		idle_add(self.__close, save_file)
		return False

	def __saved_cb(self, manager, data):
		if self.__session_id != tuple(data[0]): return False
		self.__error = False
		from gobject import idle_add
		if self.__quit: idle_add(self.__destroy)
		return False

	def __error_cb(self, manager, data):
		if self.__session_id != tuple(data[0]): return False
		self.__error = True
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False
