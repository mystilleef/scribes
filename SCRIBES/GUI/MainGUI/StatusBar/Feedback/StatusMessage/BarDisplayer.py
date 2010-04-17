from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "update-message", self.__show_cb)
		self.connect(manager, "show-message", self.__show_cb)
		self.connect(manager, "fallback", self.__hide_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bar = editor.get_data("MessageBar")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __show(self):
		self.__bar.show()
		return False
	
	def __hide(self):
		self.__bar.hide()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show, priority=9999)
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False
