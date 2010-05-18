from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

get_offset_at_mark = lambda _buffer, mark: _buffer.get_iter_at_mark(mark).get_offset()

class Navigator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "marked-matches", self.__matches_cb)
		self.connect(manager, "select-next-match", self.__next_cb)
		self.connect(manager, "select-previous-match", self.__previous_cb)
		self.connect(manager, "reset", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		from collections import deque
		self.__next_queue = deque([])
		self.__prev_queue = deque([])
		self.__current_match = None
		self.__marks = deque()
		return

	def __clear(self):
		self.__current_match = None
		self.__next_queue.clear()
		self.__prev_queue.clear()
		return

	def __navigate(self, function):
		try:
			if not self.__current_match: raise ValueError
			if len(self.__marks) == 1: raise AssertionError
			# function is either __process_next or __process_previous
			function()
		except ValueError:
			self.__manager.emit("research")
		except AssertionError:
			message = _("No other matches found")
			self.__editor.update_message(message, "fail", 10)
		return False

	def __calculate_match(self, cursor_offset, direction="next"):
		self.__next_queue.clear()
		self.__prev_queue.clear()
		pappend = lambda mark: self.__prev_queue.appendleft(mark)
		nappend = lambda mark: self.__next_queue.append(mark)
		for marks in self.__marks:
			self.__editor.response()
			mark = marks[1]
			pappend(marks) if cursor_offset > get_offset_at_mark(self.__buffer, mark) else nappend(marks)
		if direction == "next":
			match = self.__next_queue.popleft() if self.__next_queue else self.__prev_queue.popleft()
		else:
			match = self.__prev_queue.popleft() if self.__prev_queue else self.__next_queue.popleft()
		return match

	def __swap(self):
		from collections import deque
		if not self.__next_queue:
			self.__next_queue = deque(reversed(self.__prev_queue))
			self.__prev_queue = deque()
		else:
			self.__prev_queue = deque(reversed(self.__next_queue))
			self.__next_queue = deque()
		return

	def __process_next(self):
		if not self.__next_queue: self.__swap()
		if self.__current_match: self.__prev_queue.appendleft(self.__current_match)
		match = self.__next_queue.popleft()
		cursor_offset = self.__editor.cursor.get_offset()
		match = match if cursor_offset == get_offset_at_mark(self.__buffer, self.__current_match[0]) else self.__calculate_match(cursor_offset)
		self.__current_match = match
		self.__manager.emit("current-match", match)
		return False

	def __process_previous(self):
		if not self.__prev_queue: self.__swap()
		if self.__current_match: self.__next_queue.appendleft(self.__current_match)
		match = self.__prev_queue.popleft()
		cursor_offset = self.__editor.cursor.get_offset()
		match = match if cursor_offset == get_offset_at_mark(self.__buffer, self.__current_match[0]) else self.__calculate_match(cursor_offset, "previous")
		self.__current_match = match
		self.__manager.emit("current-match", match)
		return

	def __process(self, matches):
		self.__clear()
		self.__marks = matches
		match = self.__calculate_match(self.__editor.cursor.get_offset())
		self.__current_match = match
		self.__manager.emit("current-match", match)
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __matches_cb(self, manager, matches):
		from gobject import idle_add
		idle_add(self.__process, matches, priority=9999)
		return False

	def __next_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__navigate, self.__process_next, priority=9999)
		return False

	def __previous_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__navigate, self.__process_previous, priority=9999)
		return False

	def __reset_cb(self, *args):
		self.__clear()
		return False
