from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__sigid1 = self.connect(self.__buffer, "insert-text", self.__insert_cb, True)
		self.connect(manager, "enable-word-completion", self.__completion_cb)
		manager.emit("insertion-marks", (self.__lmark, self.__rmark))
		self.__block()
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__lmark = editor.create_left_mark()
		self.__rmark = editor.create_right_mark()
		self.__blocked = False
		return

	def __move_marks(self, iterator):
#		iterator = self.__editor.cursor
		self.__buffer.move_mark(self.__lmark, iterator)
		self.__buffer.move_mark(self.__rmark, iterator)
		return False

	def __reposition_marks(self):
		iterator = self.__editor.cursor
		self.__buffer.move_mark(self.__rmark, iterator)
		iterator = self.__backward_to_word_begin(iterator.copy())
		self.__buffer.move_mark(self.__lmark, iterator)
		return False

	def __in_mark_range(self):
		loffset = self.__buffer.get_iter_at_mark(self.__lmark).get_offset()
		roffset = self.__buffer.get_iter_at_mark(self.__rmark).get_offset()
		iterator = self.__editor.cursor
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

	def __block(self):
		if self.__blocked: return False
		self.__buffer.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__buffer.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __compile(self):
		methods = (
			self.__insert_cb, self.__backward_to_word_begin, self.__move_marks,
			self.__in_mark_range, self.__reposition_marks,
		)
		self.__editor.optimize(methods)
		return False

	def __completion_cb(self, manager, enable_word_completion):
		self.__unblock() if enable_word_completion else self.__block()
		if enable_word_completion: self.__reposition_marks()
		return False

	def __insert_cb(self, textbuffer, iterator, text, length):
		from Utils import is_delimeter
		if not is_delimeter(iterator.get_char()): return False
#		if not is_delimeter(self.__editor.cursor.get_char()): return False
#		is_delimeter
		if is_delimeter(text):
			self.__move_marks(iterator.copy())
		else:
			if self.__in_mark_range() is False: self.__reposition_marks()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		self.__editor.delete_mark(self.__lmark)
		self.__editor.delete_mark(self.__rmark)
		del self
		return False
