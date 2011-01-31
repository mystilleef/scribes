from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "mark-bracket-region", self.__mark_cb)
		manager.set_data("BracketRegionMarks", (self.__lmark, self.__rmark))

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__lmark = editor.create_left_mark()
		self.__rmark = editor.create_right_mark()
		return

	def __mark_cb(self, manager, bracket_region):
		self.__buffer.move_mark(self.__rmark, bracket_region[1])
		self.__buffer.move_mark(self.__lmark, bracket_region[0])
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
