from SCRIBES.SignalConnectionManager import SignalManager

class Saver(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "close", self.__close_cb)
		self.__sigid1 = self.connect(editor, "window-focus-out", self.__out_cb)
		self.connect(manager, "save-failed", self.__failed_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__error = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __save(self):
		try:
			if self.__error: raise AssertionError
			if not self.__editor.modified: return False
			self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		except AssertionError:
			self.__error = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __out_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__save, priority=9999)
		return False

	def __close_cb(self, *args):
		self.__editor.handler_block(self.__sigid1)
		return False

	def __failed_cb(self, *args):
		self.__error = True
		return False
