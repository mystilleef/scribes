from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "save-file", self.__save_cb)
		self.connect(manager, "saved?", self.__saved_cb)
		self.__sigid1 = self.connect(editor.textbuffer, "changed", self.__changed_cb)
		self.__block()
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__modified = False
		self.__blocked = False
		return

	def __emit(self, data):
		if self.__modified is False:
			self.__block()
			from gobject import idle_add
			idle_add(self.__manager.emit, "saved", data)
		else:
			self.__modified = False
			from gobject import idle_add
			idle_add(self.__manager.emit, "reset-modification-flag")
		return False

	def __block(self):
		if self.__blocked: return False
		self.__editor.textbuffer.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__editor.textbuffer.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __save_cb(self, *args):
		self.__unblock()
		return False

	def __saved_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__emit, data)
		return False

	def __changed_cb(self, *args):
		self.__modified = True
		self.__block()
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
