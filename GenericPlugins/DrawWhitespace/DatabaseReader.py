from SCRIBES.SignalConnectionManager import SignalManager

class Reader(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "database-updated", self.__updated_cb)
		self.__read()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __read(self):
		from Metadata import get_value
		self.__manager.emit("show-whitespaces", get_value())
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __updated_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__read, priority=PRIORITY_LOW)
		return False
