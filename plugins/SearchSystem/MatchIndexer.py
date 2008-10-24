from gettext import gettext as _

class Indexer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marked-matches", self.__marked_matches_cb)
		self.__sigid3 = manager.connect("current-match", self.__current_match_cb)
		self.__sigid4 = manager.connect("reset", self.__reset_cb)
		self.__sigid5 = manager.connect("hide-bar", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__matches = deque()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return

	def __get_count(self, match):
		count = 0
		for match_ in self.__matches:
			if match == match_: break
			count += 1
		return count + 1

	def __send_index(self, match):
		if not self.__matches: return
		count = self.__get_count(match)
		index = count, len(self.__matches)
		self.__manager.emit("match-index", index)
		message = _("Match %d of %d") % (index[0], index[1])
		self.__editor.update_message(message, "pass", 10)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marked_matches_cb(self, manager, matches):
		from collections import deque
		self.__matches = deque(matches)
		return False

	def __current_match_cb(self, manager, match):
		self.__send_index(match)
		return False

	def __reset_cb(self, *args):
		self.__matches.clear()
		return False
