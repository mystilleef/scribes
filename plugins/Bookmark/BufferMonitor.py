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

	def __get_marks(self, mark):
		marks = []
		marks.append(mark)
		while True:
			mark = mark.next("scribes_bookmark")
			if not mark: break
			marks.append(mark)
		return marks

	def __send_marked_lines(self):
		try:
			iterator = self.__buffer.get_bounds()[0]
			found = self.__buffer.forward_iter_to_source_mark(iterator, "scribes_bookmark")
			if found is False: raise ValueError
			mark = self.__buffer.get_source_marks_at_iter(iterator, "scribes_bookmark")[0]
			marks = self.__get_marks(mark)
			get_line = lambda iterator: iterator.get_line()
			get_iter = self.__buffer.get_iter_at_mark
			data = [get_line(get_iter(mark)) for mark in marks]
		except ValueError:
			data = []
		self.__manager.emit("marked-lines", tuple(data))
		return False

	def __destroy(self):
		self.__send_marked_lines()
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