from SCRIBES.SignalConnectionManager import SignalManager

class Writer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "toggle-error-check", self.__check_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __write(self):
		from Metadata import get_value, set_value
		set_value(not get_value())
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __check_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__write, priority=PRIORITY_LOW)
		return False
