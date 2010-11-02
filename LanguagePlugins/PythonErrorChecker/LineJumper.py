from SCRIBES.SignalConnectionManager import SignalManager

class Jumper(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "error-data", self.__error_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "remote-file-error", self.__remote_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__active = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __jump(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line-1)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.refresh(True)
		self.__editor.move_view_to_cursor(True, iterator.copy())
		self.__editor.refresh(True)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, manager, error_data):
		if self.__active is False: return False
		self.__active = False
		lineno = error_data[0]
		if not lineno: return False
		self.__jump(lineno)
		return False

	def __activate_cb(self, *args):
		from Exceptions import FileSaveError
		try:
			self.__active = True
			self.__manager.emit("check-message")
			if self.__editor.buf.get_modified() is True: raise FileSaveError
			self.__manager.emit("check")
		except (FileSaveError):
			self.__editor.save_file(self.__editor.uri)
		return False

	def __no_cb(self, *args):
		self.__active = False
		return False

	def __remote_cb(self, *args):
		self.__active = False
		self.__manager.emit("remote-file-message")
		return False
