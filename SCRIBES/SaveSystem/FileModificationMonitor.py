class Monitor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("save-file", self.__save_cb)
		self.__sigid3 = manager.connect("saved?", self.__saved_cb)
		self.__sigid4 = editor.textbuffer.connect("changed", self.__changed_cb)
		self.__block_change_signal()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__modified = False
		self.__blocked = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit(self, data):
		try:
			if self.__modified: raise ValueError
			self.__block_change_signal()
			self.__manager.emit("saved", data)
		except ValueError:
			self.__modified = False
			self.__manager.emit("reset-modification-flag")
#			print "Modification occurred while saving! Saving later!"
		return False

	def __block_change_signal(self):
		if self.__blocked: return False
		self.__editor.textbuffer.handler_block(self.__sigid4)
		self.__blocked = True
		return False

	def __unblock_change_signal(self):
		if self.__blocked is False: return False
		self.__editor.textbuffer.handler_unblock(self.__sigid4)
		self.__blocked = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __save_cb(self, *args):
		self.__unblock_change_signal()
		return False

	def __saved_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__emit, data)
		return False

	def __changed_cb(self, *args):
		self.__modified = True
		self.__block_change_signal()
		return False
