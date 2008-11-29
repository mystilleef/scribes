class Marker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("case", self.__case_cb)
		self.__sigid3 = manager.connect("complete", self.__complete_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = []
		self.__pattern = self.__editor.word_pattern
		return

	def __destroy(self):
		self.__clear()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __get_bounds(self, cursor):
		forward = False
		end = cursor.copy()
		while self.__pattern.match(end.get_char()): end.forward_char()
		start = end.copy()
		start.backward_char()
		while self.__pattern.match(start.get_char()):
			forward = False
			if start.starts_line(): break
			if not start.backward_char(): break
			forward = True
		if forward: start.forward_char()
		return start, end

	def __get_word_bounds(self):
		try:
			bound = None
			cursor = self.__editor.cursor
			from Exceptions import NoTextFoundError
			if self.__pattern.match(cursor.get_char()): raise ValueError
			if cursor.starts_line(): raise NoTextFoundError
			if not cursor.backward_char(): raise NoTextFoundError
			if self.__pattern.match(cursor.get_char()): raise ValueError
			raise NoTextFoundError
		except ValueError:
			bound = self.__get_bounds(cursor)
		return bound

	def __send_word_bounds(self):
		try:
			from Exceptions import NoTextFoundError
			bound = self.__get_word_bounds()
			self.__send(bound)
		except NoTextFoundError:
			message = _("No text found")
			self.__editor.update_message(message, "fail", 10)
		return False

	def __send_marks(self):
		try:
			from Exceptions import NoSelectionFoundError
			if not self.__editor.selection_range: raise NoSelectionFoundError
			bound = self.__editor.selection_bounds
			self.__send(bound)
		except NoSelectionFoundError:
			self.__send_word_bounds()
		return False

	def __send(self, bound):
		lmark=self.__editor.create_left_mark(bound[0])
		rmark=self.__editor.create_right_mark(bound[1])
		self.__marks.append(lmark)
		self.__marks.append(rmark)
		self.__manager.emit("marks", (lmark, rmark))
		return False

	def __clear(self):
		for mark in self.__marks: self.__editor.delete_mark(mark)
		self.__marks = []
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __case_cb(self, *args):
		self.__send_marks()
		return False

	def __complete_cb(self, *args):
		self.__clear()
		return False
