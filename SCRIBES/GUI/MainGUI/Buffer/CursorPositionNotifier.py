class Notifier(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__buffer.notify("cursor-position")
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__buffer.connect("notify::cursor-position", self.__position_cb)
		self.__sigid3 = self.__editor.connect("checking-file", self.__block_cb)
		self.__sigid4 = self.__editor.connect("loaded-file", self.__unblock_cb)
		self.__sigid5 = self.__editor.connect("load-error", self.__unblock_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __notify(self):
		self.__editor.emit("cursor-moved")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __position_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__notify, priority=99999)
		return False

	def __block_cb(self, *args):
		self.__buffer.handler_block(self.__sigid2)
		return False

	def __unblock_cb(self, *args):
		self.__buffer.handler_unblock(self.__sigid2)
		return False
