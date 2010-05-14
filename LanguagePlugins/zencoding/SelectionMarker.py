from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__quit_cb)
		self.connect(manager, "mark-selection", self.__mark_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bmark = editor.create_left_mark()
		self.__emark = editor.create_right_mark()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __mark(self):
		try:
			if not self.__editor.has_selection: raise ValueError
			start_iterator, end_iterator = self.__editor.selection_bounds
			self.__editor.textbuffer.move_mark(self.__bmark, start_iterator)
			self.__editor.textbuffer.move_mark(self.__emark, end_iterator)
			self.__manager.emit("selection-marks", (self.__bmark, self.__emark))
		except ValueError:
			self.__manager.emit("selection-marks", (None, None))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __mark_cb(self, *args):
		self.__mark()
		return False
