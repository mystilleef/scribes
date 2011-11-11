from SCRIBES.SignalConnectionManager import SignalManager

class Notifier(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.__buffer.notify("cursor-position")
		self.connect(editor, "quit", self.__quit_cb)
		self.__sigid2 = self.connect(self.__buffer, "notify::cursor-position", self.__position_cb)
		self.connect(editor, "checking-file", self.__block_cb)
		self.connect(editor, "loaded-file", self.__unblock_cb)
		self.connect(editor, "load-error", self.__unblock_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __position_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__editor.emit, "cursor-moved")
		return False

	def __block_cb(self, *args):
		self.__buffer.handler_block(self.__sigid2)
		return False

	def __unblock_cb(self, *args):
		self.__buffer.handler_unblock(self.__sigid2)
		return False
