from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "exit-sparkup-mode", self.__remove_cb, True)
		self.connect(manager, "remove-marks", self.__remove_cb)
		self.connect(manager, "placeholder-offsets", self.__offsets_cb)
		self.connect(manager, "execute", self.__execute_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = {}
		return

	def __create_boundary_marks(self):
		lmark = self.__editor.create_left_mark()
		rmark = self.__editor.create_right_mark()
		self.__update_marks(lmark)
		self.__update_marks(rmark)
		self.__manager.emit("boundary-marks", (lmark, rmark))
		return False

	def __update_marks(self, mark):
		nesting_level = len(self.__marks)
		self.__marks[nesting_level].append(mark)
		return False

	def __del(self, mark):
		self.__editor.refresh(False)
		mark.set_visible(False)
		self.__editor.delete_mark(mark)
		self.__editor.refresh(False)
		return False

	def __remove_marks(self):
		self.__editor.freeze()
		[self.__del(mark) for mark in self.__marks[len(self.__marks)]]
		del self.__marks[len(self.__marks)]
		self.__editor.thaw()
		return False

	def __offset_to_mark(self, offset, left=True):
		iterator = self.__editor.textbuffer.get_iter_at_offset(offset)
		ed = self.__editor
		create_mark = ed.create_left_mark if left else ed.create_right_mark
		mark = create_mark(iterator)
		mark.set_visible(True)
		return mark

	def __marks_from(self, offsets):
		otm = self.__offset_to_mark
		marks = [(otm(start, True), otm(end, False)) for start, end in offsets]
		update = self.__update_marks
		[(update(smark), update(emark)) for smark, emark in marks]
		self.__manager.emit("placeholder-marks", marks)
		return False

	def __execute_cb(self, *args):
		nesting_level = len(self.__marks) + 1
		self.__marks[nesting_level] = []
		self.__create_boundary_marks()
		return False

	def __remove_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__remove_marks, priority=PRIORITY_LOW)
		return False

	def __offsets_cb(self, manager, offsets):
		self.__marks_from(offsets)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
