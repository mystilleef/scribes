from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "message-bar-is-updated", self.__update_cb)
		self.connect(manager, "reset", self.__fallback_cb)
		self.connect(manager, "fallback", self.__fallback_cb)
		self.__editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bar = editor.get_data("MessageBar")
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update_cb(self, manager, data):
		show_bar = data[-1]
		if show_bar: self.__bar.show()
		return False

	def __fallback_cb(self, *args):
		self.__bar.hide()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
