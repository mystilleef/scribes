from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__buffer, "insert-text", self.__insert_cb, True)
		manager.emit("insertion-marks", (self.__lmark, self.__rmark))

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__lmark = editor.create_left_mark()
		self.__rmark = editor.create_right_mark()
		return

	def __move_marks_to(self, iterator):
		self.__buffer.move_mark(self.__lmark, iterator)
		self.__buffer.move_mark(self.__rmark, iterator)
		return False

	def __reposition_marks(self, iterator):
		self.__buffer.move_mark(self.__rmark, iterator)
		iterator = self.__backward_to_word_begin(iterator.copy())
		self.__buffer.move_mark(self.__lmark, iterator)
		return False

	def __in_mark_range(self, iterator):
		loffset = self.__buffer.get_iter_at_mark(self.__lmark).get_offset()
		roffset = self.__buffer.get_iter_at_mark(self.__rmark).get_offset()
		ioffset = iterator.get_offset()
		return loffset <= ioffset <= roffset

	def __backward_to_word_begin(self, iterator):
		if iterator.starts_line(): return iterator
		iterator.backward_char()
		from Utils import is_delimeter
		while not is_delimeter(iterator.get_char()):
			iterator.backward_char()
			if iterator.starts_line(): return iterator
		iterator.forward_char()
		return iterator

	def __insert_cb(self, textbuffer, iterator, text, length):
		from Utils import is_delimeter
		if not is_delimeter(iterator.get_char()): return False
		if is_delimeter(text):
			self.__move_marks_to(iterator)
		else:
			if self.__in_mark_range(iterator) is False: self.__reposition_marks(iterator)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		self.__editor.delete_mark(self.__lmark)
		self.__editor.delete_mark(self.__rmark)
		del self
		return False
