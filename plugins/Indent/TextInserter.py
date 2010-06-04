from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "processed-text", self.__text_cb)
		self.connect(manager, "marks", self.__marks_cb)
		self.connect(manager, "complete", self.__complete_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		return 

	def __destroy(self):
		self.disconnect()
		del self
		return 

	def __insert(self, text):
		start = self.__editor.textbuffer.get_iter_at_mark(self.__marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(self.__marks[1])
		self.__editor.textview.window.freeze_updates()
		self.__editor.textbuffer.delete(start, end)
		self.__editor.textbuffer.insert_at_cursor(text)
		self.__editor.textview.window.thaw_updates()
		self.__manager.emit("inserted-text")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __text_cb(self, manager, text):
		self.__insert(text)
		return False

	def __marks_cb(self, manager, marks):
		self.__marks = marks
		return False

	def __complete_cb(self, *args):
		self.__marks = None
		return False
