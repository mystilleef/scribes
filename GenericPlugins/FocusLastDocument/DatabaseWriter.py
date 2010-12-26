from SCRIBES.SignalConnectionManager import SignalManager

class Writer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "window-focus-out", self.__out_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __write(self):
		if not self.__editor.uri: return False
		from Metadata import set_value
		set_value(self.__editor.uri)
		return False

	def __out_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__write, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
