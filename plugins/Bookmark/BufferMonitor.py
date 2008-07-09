class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__buffer.connect("source-mark-updated", self.__updated_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __find_first_mark(self):
		iterator = self.__buffer.get_bounds()[0]
		marks = self.__buffer.get_source_marks_at_iter(iterator, "scribes_bookmark")
		if marks: return marks[0]
		found_mark = self.__buffer.forward_iter_to_source_mark(iterator, "scribes_bookmark")
		if found_mark is False: raise ValueError
		marks = self.__buffer.get_source_marks_at_iter(iterator, "scribes_bookmark")
		return marks[0]

	def __get_all_marks(self, mark):
		marks = []
		append = marks.append
		append(mark)
		while True:
			mark = mark.next("scribes_bookmark")
			if mark is None: break
			append(mark)
		return marks

	def __get_lines_from_marks(self, marks):
		iter_at_mark = self.__buffer.get_iter_at_mark
		get_line_from_mark = lambda mark: iter_at_mark(mark).get_line()
		lines = [get_line_from_mark(mark) for mark in marks]
		return lines

	def __send_marked_lines(self):
		try:
			mark = self.__find_first_mark()
			marks = self.__get_all_marks(mark)
			lines = self.__get_lines_from_marks(marks)
		except ValueError:
			lines = []
		finally:
			self.__manager.emit("marked-lines", tuple(lines))
			self.__editor.refresh()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_cb(self, *args):
		self.__send_marked_lines()
		return False
