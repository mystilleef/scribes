from SCRIBES.SignalConnectionManager import SignalManager

class Notifier(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "checking-file", self.__block_cb)
		self.connect(editor, "loaded-file", self.__unblock_cb)
		self.connect(editor, "load-error", self.__unblock_cb)
		self.__sigid1 = self.connect(self.__buffer, "modified-changed", self.__modified_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __block_cb(self, *args):
		self.__buffer.handler_block(self.__sigid1)
		return False

	def __unblock_cb(self, *args):
		self.__buffer.handler_unblock(self.__sigid1)
		return False

	def __modified_cb(self, *args):
		modified = self.__buffer.get_modified()
		from gobject import idle_add
		idle_add(self.__editor.emit, "modified-file", modified)
		return False
