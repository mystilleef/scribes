from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "toggle", self.__toggle_cb)
		self.connect(manager, "lines", self.__lines_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__lines = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __toggle(self):
		line = self.__editor.cursor.get_line()
		emit = self.__manager.emit
		emit("remove", line) if line in self.__lines else emit("add", line)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggle_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__toggle)
		return False

	def __lines_cb(self, manager, lines):
		self.__lines = lines
		return False
