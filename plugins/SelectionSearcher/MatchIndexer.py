from SCRIBES.SignalConnectionManager import SignalManager
from gettext import gettext as _

class Indexer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "marked-matches", self.__marked_matches_cb)
		self.connect(manager, "current-match", self.__current_match_cb)
		self.connect(manager, "reset", self.__reset_cb)
		editor.response()

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
		message = _("Removed selection highlights")
		if len(self.__matches) > 1: self.__editor.update_message(message, "yes", 3)
		self.__matches.clear()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marked_matches_cb(self, manager, matches):
		from collections import deque
		self.__matches = deque(matches)
		return False

	def __current_match_cb(self, manager, match):
		from gobject import idle_add
		idle_add(self.__send_index, match)
#		self.__send_index(match)
		return False

	def __reset_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__reset, priority=9999)
		return False
