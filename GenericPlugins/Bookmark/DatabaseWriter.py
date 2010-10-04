from SCRIBES.SignalConnectionManager import SignalManager

class Writer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb, True)
		self.connect(manager, "lines", self.__lines_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, lines):
		uri = self.__editor.uri
		if not uri: return False
		from Metadata import set_value
		self.__editor.response()
		set_value(str(uri), lines)
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __lines_cb(self, manager, lines):
		from gobject import idle_add
		idle_add(self.__update, lines)
		return False
