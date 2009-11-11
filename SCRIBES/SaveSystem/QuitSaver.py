class Saver(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("close", self.__close_cb)
		self.__sigid2 = manager.connect("save-succeeded", self.__saved_cb)
		self.__sigid3 = manager.connect("save-failed", self.__error_cb)
		self.__sigid4 = manager.connect("session-id", self.__session_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		self.__quit = False
		self.__error = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		self.__editor.emit("quit")
		del self
		self = None
		return False

	def __save(self):
		self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		return False

	def __close(self, save_file):
		try:
			if save_file is False: raise StandardError
			if self.__error: raise ValueError
			if self.__editor.modified is False: raise ValueError
			self.__quit = True
			#if not self.__editor.uri: raise StandardError
			from gobject import idle_add
			idle_add(self.__save, priority=9999)
		except ValueError:
			self.__destroy()
		except StandardError:
			self.__manager.emit("remove-new-file")
			self.__destroy()
		return False

	def __close_cb(self, editor, save_file):
		from gobject import idle_add
		idle_add(self.__close, save_file, priority=9999)
		return False

	def __saved_cb(self, manager, data):
		if self.__session_id != tuple(data[0]): return False
		self.__error = False
		if self.__quit: self.__destroy()
		return False

	def __error_cb(self, manager, data):
		if self.__session_id != tuple(data[0]): return False
		self.__error = True
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False
