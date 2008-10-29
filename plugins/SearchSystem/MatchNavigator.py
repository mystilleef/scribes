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

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__next_queue = deque([])
		self.__prev_queue = deque([])
		self.__current_match = None
		self.__backward_flag = False
		return 

	def __clear(self):
		self.__next_queue.clear()
		self.__prev_queue.clear()
		return 

	def __process_next(self):
		try:
			if not self.__next_queue: raise ValueError
			self.__prev_queue.appendleft(self.__current_match)
			match = self.__next_queue.popleft()
			self.__current_match = match
			self.__manager.emit("current-match", match)
		except ValueError:
			message = _("No next match found")
			self.__editor.update_message(message, "fail", 10)
		return False

	def __process_previous(self):
		try:
			if not self.__prev_queue: raise ValueError
			self.__next_queue.appendleft(self.__current_match)
			match = self.__prev_queue.popleft()
			self.__current_match = match
			self.__manager.emit("current-match", match)
		except ValueError:
			message = _("No previous match found")
			self.__editor.update_message(message, "fail", 10)
		return

	def __process(self, matches):
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

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marked_matches_cb(self, manager, matches):
		self.__process(matches)
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
