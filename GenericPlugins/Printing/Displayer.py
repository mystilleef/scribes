from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(self.__manager, "destroy", self.__destroy_cb)
		self.connect(self.__manager, "activate", self.__activate_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate(self):
		self.__editor.response()
		from Printer import Printer
		Printer(self.__manager, self.__editor).show()
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate, priority=9999)
		return False
