class Inserter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marks", self.__marks_cb)
		self.__sigid3 = manager.connect("processed-text", self.__text_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __insert(self, string):
		start = self.__buffer.get_iter_at_mark(self.__marks[0])
		end = self.__buffer.get_iter_at_mark(self.__marks[1])
		self.__buffer.delete(start, end)
		self.__buffer.begin_user_action()
		self.__buffer.insert_at_cursor(string)
		self.__buffer.end_user_action()
		self.__manager.emit("text-inserted")
		self.__marks = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marks_cb(self, manager, marks):
		self.__marks = marks
		return False

	def __text_cb(self, manager, string):
		self.__insert(string)
		return False
