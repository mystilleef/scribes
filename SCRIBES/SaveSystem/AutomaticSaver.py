from SCRIBES.SignalConnectionManager import SignalManager

SAVE_TIMER = 7000

class Saver(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.__sigid1 = self.connect(editor, "modified-file", self.__modified_cb)
		self.connect(editor, "close", self.__close_cb)
		self.connect(manager, "reset-modification-flag", self.__modified_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__remove_timer()
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __process(self):
		self.__remove_timer()
		from gobject import timeout_add
		self.__timer = timeout_add(SAVE_TIMER, self.__save_on_idle, priority=9999)
		return False

	def __save_on_idle(self):
		from gobject import idle_add
		idle_add(self.__save, priority=9999)
		return False

	def __save(self):
		if self.__editor.modified is False: return False
		self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __close_cb(self, *args):
		self.__remove_timer()
		self.__editor.handler_block(self.__sigid1)
		return False

	def __modified_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__process)
		return False
