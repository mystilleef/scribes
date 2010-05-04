from SCRIBES.SignalConnectionManager import SignalManager

class Extractor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "marks", self.__marks_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __send_text(self, marks):
		start = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(marks[1])
		text = self.__editor.textbuffer.get_text(start, end)
		self.__manager.emit("extracted-text", text)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marks_cb(self, manager, marks):
		self.__send_text(marks)
		return False
