from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "offsets", self.__process_cb)
		self.connect(manager, "complete", self.__complete_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		return

	def __destroy(self):
		self.__clear()
		self.disconnect()
		del self
		return 

	def __clear(self):
		if not self.__marks: return
		self.__editor.delete_mark(self.__marks[0])
		self.__editor.delete_mark(self.__marks[1])
		self.__marks = None
		return False

	def __iter_from_selection(self, offsets):
		get_iter = self.__editor.textbuffer.get_iter_at_line_offset
		start = get_iter(offsets[0][0], offsets[0][1])
		end = get_iter(offsets[1][0], offsets[1][1])
		start = self.__editor.backward_to_line_begin(start.copy())
		end = self.__editor.forward_to_line_end(end.copy())
		return start, end

	def __iter_from_cursor(self):
		start = self.__editor.backward_to_line_begin()
		end = self.__editor.forward_to_line_end(start.copy())
		return start, end

	def __send_marks(self, offsets):
		start, end = self.__iter_from_selection(offsets) if len(offsets) > 1 else self.__iter_from_cursor()
		bmark = self.__editor.create_left_mark(start)
		emark = self.__editor.create_right_mark(end)
		self.__marks = bmark, emark
		self.__manager.emit("marks", (bmark, emark))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, manager, offsets):
		self.__send_marks(offsets)
		return False

	def __complete_cb(self, *args):
		self.__clear()
		return False
