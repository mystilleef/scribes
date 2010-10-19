from gettext import gettext as _

class Navigator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marked-matches", self.__marked_matches_cb)
		self.__sigid3 = manager.connect("next", self.__next_cb)
		self.__sigid4 = manager.connect("previous", self.__previous_cb)
		self.__sigid5 = manager.connect("reset", self.__clear_cb)
		self.__sigid6 = manager.connect("search-type-flag", self.__search_type_cb)
		self.__sigid7 = manager.connect("replaced-mark", self.__replaced_mark_cb)
		self.__sigid8 = manager.connect("cursor-mark", self.__cursor_mark_cb)

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
		return

	def __process_next(self):
		if not self.__next_queue: self.__swap()
		if self.__current_match: self.__prev_queue.appendleft(self.__current_match)
		match = self.__next_queue.popleft()
		self.__current_match = match
		self.__manager.emit("current-match", match)
		return False

	def __process_previous(self):
		if not self.__prev_queue: self.__swap()
		if self.__current_match: self.__next_queue.appendleft(self.__current_match)
		match = self.__prev_queue.popleft()
		self.__current_match = match
		self.__manager.emit("current-match", match)
		return

	def __old_navigation_behavior(self, matches):
		self.__clear()
		from collections import deque
		if self.__backward_flag:
			match = matches[-1]
			matches = matches[:-1]
			matches.reverse()
			self.__prev_queue = deque(matches)
		else:
			self.__next_queue = deque(matches)
			match = self.__next_queue.popleft()
		self.__current_match = match
		self.__manager.emit("current-match", match)
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
		self.__manager.emit("current-match", match)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marked_matches_cb(self, manager, matches):
		self.__process(matches)
#		self.__default(matches)
		return False

	def __next_cb(self, *args):
		self.__process_next()
		return False

	def __previous_cb(self, *args):
		self.__process_previous()
		return False

	def __clear_cb(self, *args):
		self.__clear()
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
