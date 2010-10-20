from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.__sigid1 = self.connect(self.__buffer, "changed", self.__response_cb)
		self.__sigid2 = self.connect(self.__buffer, "changed", self.__response_cb, True)
		self.__sigid3 = self.connect(self.__buffer, "highlight-updated", self.__response_cb)
		self.__sigid4 = self.connect(self.__buffer, "highlight-updated", self.__response_cb, True)
#		self.__sigid5 = self.connect(self.__buffer, "source-mark-updated", self.__response_cb)
#		self.__sigid6 = self.connect(self.__buffer, "source-mark-updated", self.__response_cb, True)
		self.connect(editor, "quit", self.__quit_cb)
#		self.connect(editor, "checking-file", self.__checking_cb)
#		self.connect(editor, "loaded-file", self.__loaded_cb, True)
#		self.connect(editor, "load-error", self.__loaded_cb, True)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__is_blocked = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __block(self):
		if self.__is_blocked: return
		self.__buffer.handler_block(self.__sigid1)
		self.__buffer.handler_block(self.__sigid2)
		self.__buffer.handler_block(self.__sigid3)
		self.__buffer.handler_block(self.__sigid4)
		self.__buffer.handler_block(self.__sigid5)
		self.__buffer.handler_block(self.__sigid6)
		self.__is_blocked = True
		return

	def __unblock(self):
		if self.__is_blocked is False: return False
		self.__buffer.handler_unblock(self.__sigid1)
		self.__buffer.handler_unblock(self.__sigid2)
		self.__buffer.handler_unblock(self.__sigid3)
		self.__buffer.handler_unblock(self.__sigid4)
		self.__buffer.handler_unblock(self.__sigid5)
		self.__buffer.handler_unblock(self.__sigid6)
		self.__is_blocked = False
		return False

	def __refresh(self):
		self.__editor.refresh(False)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __response_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__refresh)
		return False

	def __checking_cb(self, *args):
		self.__block()
		return False

	def __loaded_cb(self, *args):
		from gobject import timeout_add
		timeout_add(1000, self.__unblock, priority=99999)
		return False
