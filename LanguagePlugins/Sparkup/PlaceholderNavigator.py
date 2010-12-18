from SCRIBES.SignalConnectionManager import SignalManager

class Navigator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "next-placeholder", self.__next_cb)
		self.connect(manager, "previous-placeholder", self.__previous_cb)
		self.connect(manager, "removed-placeholders", self.__removed_cb)
		self.connect(manager, "exit-sparkup-mode", self.__exit_cb)
		self.connect(manager, "placeholder-marks", self.__marks_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__marks = {}
		self.__nesting_level = 0
		return

	def __select_first_placeholder(self):
		first_marks = self.__marks[self.__nesting_level][0]
		self.__select(first_marks)
		return False

	def __get_offset_from(self, mark):
		gifm = self.__buffer.get_iter_at_mark
		return gifm(mark).get_offset()

	def __select_next_placeholder(self):
		self.__editor.freeze()
		offset = self.__editor.cursor.get_offset()
		gof = self.__get_offset_from
		next_marks = ()
		for smark, emark in self.__marks[self.__nesting_level]:
			self.__editor.refresh(False)
			if gof(smark) <= offset: continue
			next_marks = smark, emark
			break
		emit = self.__manager.emit
		self.__select(next_marks) if next_marks else emit("exit-sparkup-mode")
		self.__editor.thaw()
		return False

	def __select_previous_placeholder(self):
		self.__editor.freeze()
		offset = self.__editor.cursor.get_offset()
		gof = self.__get_offset_from
		previous_marks = ()
		marks = self.__marks[self.__nesting_level]
		for smark, emark in reversed(marks):
			self.__editor.refresh(False)
			if gof(emark) >= offset: continue
			previous_marks = smark, emark
			break
		self.__select(previous_marks) if previous_marks else self.__select(marks[-1])
		self.__editor.thaw()
		return False

	def __select(self, marks):
		gifm = self.__buffer.get_iter_at_mark
		start, end = gifm(marks[0]), gifm(marks[1])
		self.__buffer.select_range(start, end)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __marks_cb(self, manager, marks):
		self.__nesting_level += 1
		self.__marks[self.__nesting_level] = marks
		return False

	def __exit_cb(self, *args):
		del self.__marks[self.__nesting_level]
		self.__nesting_level -= 1
		if self.__nesting_level < 0: self.__nesting_level = 0
		return False

	def __removed_cb(self, *args):
		self.__select_first_placeholder()
		return False

	def __next_cb(self, *args):
		self.__select_next_placeholder()
		return False

	def __previous_cb(self, *args):
		self.__select_previous_placeholder()
		return False
