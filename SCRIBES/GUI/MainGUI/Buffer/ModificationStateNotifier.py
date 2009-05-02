class Notifier(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__block_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__unblock_cb)
		self.__sigid4 = editor.connect("load-error", self.__unblock_cb)
		self.__sigid5 = self.__buffer.connect("modified-changed", self.__modified_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__buffer)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit(self):
		modified = self.__buffer.get_modified()
		self.__editor.emit("modified-file", modified)
		return False

	def __block_signal(self):
		self.__buffer.handler_block(self.__sigid5)
		return False

	def __unblock_signal(self):
		self.__buffer.handler_unblock(self.__sigid5)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __block_cb(self, *args):
		self.__block_signal()
		return False

	def __unblock_cb(self, *args):
		self.__unblock_signal()
		return False

	def __modified_cb(self, *args):
		self.__emit()
		return False
