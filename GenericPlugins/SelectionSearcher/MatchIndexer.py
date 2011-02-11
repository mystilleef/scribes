from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

class Indexer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "marked-matches", self.__marked_matches_cb)
		self.connect(manager, "current-match", self.__current_match_cb)
		self.connect(manager, "reset", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__matches = deque()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __get_count(self, match):
		count = 0
		for match_ in self.__matches:
			if match == match_: break
			count += 1
		return count + 1

	def __send_index(self, match):
		if not self.__matches or len(self.__matches) == 1: return
		count = self.__get_count(match)
		index = count, len(self.__matches)
		message = _("Match %d of %d") % (index[0], index[1])
		self.__editor.update_message(message, "yes", 10)
		return

	def __reset(self):
		self.__matches.clear()
#		message = _("Removed selection highlights")
#		if len(self.__matches) > 1: self.__editor.update_message(message, "yes", 3)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marked_matches_cb(self, manager, matches):
		from collections import deque
		self.__matches = deque(matches)
		return False

	def __current_match_cb(self, manager, match):
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer1 = idle_add(self.__send_index, match)
		return False

	def __reset_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__reset, priority=PRIORITY_LOW)
		return False
