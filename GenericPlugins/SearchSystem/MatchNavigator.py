from SCRIBES.SignalConnectionManager import SignalManager

class Navigator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "marked-matches", self.__marked_matches_cb)
		self.connect(manager, "next", self.__next_cb)
		self.connect(manager, "previous", self.__previous_cb)
		self.connect(manager, "reset", self.__clear_cb)
		self.connect(manager, "search-type-flag", self.__search_type_cb)
		self.connect(manager, "replaced-mark", self.__replaced_mark_cb)
		self.connect(manager, "cursor-mark", self.__cursor_mark_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__next_queue = deque([])
		self.__prev_queue = deque([])
		self.__current_match = None
		self.__backward_flag = False
		self.__cursor_mark = None
		return

	def __clear(self):
		self.__next_queue.clear()
		self.__prev_queue.clear()
		return

	def __swap(self):
		from collections import deque
		if not self.__next_queue:
			self.__next_queue = deque(reversed(self.__prev_queue))
			self.__prev_queue = deque()
		else:
			self.__prev_queue = deque(reversed(self.__next_queue))
			self.__next_queue = deque()
		return False

	def __process_next(self):
		if not self.__next_queue: self.__swap()
		if self.__current_match: self.__prev_queue.appendleft(self.__current_match)
		match = self.__next_queue.popleft()
		self.__current_match = match
		from gobject import idle_add
		idle_add(self.__manager.emit, "current-match", match)
		return False

	def __process_previous(self):
		if not self.__prev_queue: self.__swap()
		if self.__current_match: self.__next_queue.appendleft(self.__current_match)
		if not self.__prev_queue: return False
		match = self.__prev_queue.popleft()
		self.__current_match = match
		from gobject import idle_add
		idle_add(self.__manager.emit, "current-match", match)
		return False

	def __process(self, matches):
		self.__clear()
		get_offset = lambda mark: self.__editor.textbuffer.get_iter_at_mark(mark).get_offset()
		pappend = lambda mark: self.__prev_queue.appendleft(mark)
		nappend = lambda mark: self.__next_queue.append(mark)
		cursor_offset = get_offset(self.__cursor_mark)
		for marks in matches:
			mark = marks[0]
			pappend(marks) if cursor_offset > get_offset(mark) else nappend(marks)
		match = self.__next_queue.popleft() if self.__next_queue else self.__prev_queue.popleft()
		self.__current_match = match
		self.__editor.view.scroll_mark_onscreen(match[-1])
		from gobject import idle_add
		idle_add(self.__manager.emit, "current-match", match)
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __marked_matches_cb(self, manager, matches):
		from gobject import idle_add
		idle_add(self.__process, matches)
		return False

	def __next_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__process_next)
		return False

	def __previous_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__process_previous)
		return False

	def __clear_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__clear)
		return False

	def __search_type_cb(self, manager, search_type):
		self.__backward_flag = True if search_type == "backward" else False
		return False

	def __replaced_mark_cb(self, manager, mark):
		if mark in self.__next_queue: self.__next_queue.remove(mark)
		if mark in self.__prev_queue: self.__prev_queue.remove(mark)
		if mark == self.__current_match: self.__current_match = None
		return False

	def __cursor_mark_cb(self, manager, mark):
		self.__cursor_mark = mark
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
