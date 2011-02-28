from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "region-marks", self.__marks_cb)
		self.connect(manager, "processed", self.__processed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__lmark = None
		self.__rmark = None
		return

	def __insert(self, text):
		start, end = self.__editor.iter_at_mark(self.__lmark), self.__editor.iter_at_mark(self.__rmark)
		self.__editor.begin_user_action()
		self.__editor.textbuffer.delete(start, end)
		self.__editor.grab_focus()
		self.__editor.textbuffer.insert_at_cursor(text)
		self.__editor.grab_focus()
		self.__editor.end_user_action()
		from gobject import idle_add
		idle_add(self.__manager.emit, "inserted-text")
		return False

	def __processed_cb(self, manager, text):
		from gobject import idle_add
		idle_add(self.__insert, text)
		return False

	def __marks_cb(self, manager, marks):
		self.__lmark, self.__rmark = marks
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
