from SCRIBES.SignalConnectionManager import SignalManager

class Reseter(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "checking-file", self.__reset_cb)
		self.connect(editor, "loaded-file", self.__reset_cb)
		self.connect(editor, "load-error", self.__reset_cb)
		self.connect(editor, "saved-file", self.__reset_cb)
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

	def __reset_cb(self, *args):
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		return False
