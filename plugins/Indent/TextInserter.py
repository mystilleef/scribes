class Inserter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("processed-text", self.__text_cb)
		self.__sigid3 = manager.connect("marks", self.__marks_cb)
		self.__sigid4 = manager.connect("complete", self.__complete_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return 

	def __insert(self, text):
		start = self.__editor.textbuffer.get_iter_at_mark(self.__marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(self.__marks[1])
		self.__editor.refresh()
		self.__editor.textbuffer.delete(start, end)
		self.__editor.textbuffer.insert_at_cursor(text)
		self.__editor.refresh()
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
