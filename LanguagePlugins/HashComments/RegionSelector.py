from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "region-marks", self.__marks_cb)
		self.connect(manager, "inserted-text", self.__text_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__has_selection = False
		self.__lmark = None
		self.__rmark = None
		return

	def __select(self):
		if self.__has_selection is False: return False
		start, end = self.__editor.iter_at_mark(self.__lmark), self.__editor.iter_at_mark(self.__rmark)
		self.__editor.textbuffer.select_range(start, end)
		from gobject import idle_add
		idle_add(self.__manager.emit, "finished")
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __text_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__select)
		return False

	def __activate_cb(self, *args):
		self.__has_selection = self.__editor.has_selection
		return False

	def __marks_cb(self, manager, marks):
		self.__lmark, self.__rmark = marks
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
