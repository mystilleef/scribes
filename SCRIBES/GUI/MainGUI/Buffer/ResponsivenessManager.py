from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.connect(editor.textbuffer, "changed", self.__response_cb, data=editor)
		self.connect(editor.textbuffer, "changed", self.__response_cb, True, data=editor)
		self.connect(editor, "quit", self.__quit_cb)
		editor.register_object(self)

	def __destroy(self, editor):
		self.disconnect()
		editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, editor, *args):
		from gobject import idle_add
		idle_add(self.__destroy, editor)
		return False

	def __response_cb(self, _buffer, editor):
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(editor.refresh, priority=PRIORITY_HIGH)
		return False
