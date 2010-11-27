from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.__sigid1 = self.connect(self.__buffer, "changed", self.__response_cb)
		self.__sigid2 = self.connect(self.__buffer, "changed", self.__response_cb, True)
		self.__sigid3 = self.connect(self.__buffer, "highlight-updated", self.__response_cb)
		self.__sigid4 = self.connect(self.__buffer, "highlight-updated", self.__response_cb, True)
		self.__sigid5 = self.connect(self.__buffer, "source-mark-updated", self.__response_cb)
		self.__sigid6 = self.connect(self.__buffer, "source-mark-updated", self.__response_cb, True)
		self.connect(editor, "quit", self.__quit_cb)
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

	def __refresh(self):
		self.__editor.refresh(False)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __response_cb(self, *args):
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__refresh, priority=PRIORITY_HIGH)
		return False
