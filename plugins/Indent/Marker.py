class Marker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("indent", self.__process_cb)
		self.__sigid3 = manager.connect("unindent", self.__process_cb)
		self.__sigid4 = manager.connect("complete", self.__complete_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		return

	def __destroy(self):
		self.__clear()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return 

	def __clear(self):
		if not self.__marks: return
		self.__editor.delete_mark(self.__marks[0])
		self.__editor.delete_mark(self.__marks[1])
		self.__marks = None
		return False

	def __iter_from_selection(self):
		start, end = self.__editor.selection_bounds
		start = self.__editor.backward_to_line_begin(start.copy())
		end = self.__editor.forward_to_line_end(end.copy())
		return start, end

	def __iter_from_cursor(self):
		start = self.__editor.backward_to_line_begin()
		end = self.__editor.forward_to_line_end(start.copy())
		return start, end

	def __send_marks(self):
		selection = self.__editor.selection_range
		start, end = self.__iter_from_selection() if selection > 1 else self.__iter_from_cursor()
		bmark = self.__editor.create_left_mark(start)
		emark = self.__editor.create_right_mark(end)
		self.__marks = bmark, emark
		self.__manager.emit("marks", (bmark, emark))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, *args):
		self.__send_marks()
		return False

	def __complete_cb(self, *args):
		self.__clear()
		return False
