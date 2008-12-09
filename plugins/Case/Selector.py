class Selector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marks", self.__marks_cb)
		self.__sigid3 = manager.connect("text-inserted", self.__inserted_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __select(self):
		start = self.__editor.textbuffer.get_iter_at_mark(self.__marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(self.__marks[1])
		self.__editor.response()
		self.__editor.textbuffer.select_range(start, end)
		self.__editor.response()
		self.__manager.emit("complete")
		self.__marks = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marks_cb(self, manager, marks):
		self.__marks = marks
		return False

	def __inserted_cb(self, *args):
		self.__select()
		return False
