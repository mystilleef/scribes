from SCRIBES.SignalConnectionManager import SignalManager

class Decider(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "region-marks", self.__marks_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __decide(self, marks):
		start, end = self.__editor.iter_at_mark(marks[0]), self.__editor.iter_at_mark(marks[1])
		text = self.__editor.textbuffer.get_text(start, end)
		from gobject import idle_add
		emit = lambda signal: idle_add(self.__manager.emit, signal, text)
		emit("uncomment") if text.lstrip(" \t").startswith("#") else emit("comment")
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __marks_cb(self, manager, marks):
		from gobject import idle_add
		idle_add(self.__decide, marks)
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
