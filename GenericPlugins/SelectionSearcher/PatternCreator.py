from SCRIBES.SignalConnectionManager import SignalManager
MATCH_WORD = True

class Creator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "search", self.__search_cb)
		self.connect(manager, "research", self.__research_cb)
		self.connect(manager, "reset", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__string = ""
		self.__search_mode = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __create_pattern(self, string):
		try:
			if not string: raise ValueError
			if self.__string == string and self.__search_mode: return False
			self.__search_mode = True
			self.__string = string
			from re import escape
			string = escape(string)
			pattern = r"\b%s\b" % string if MATCH_WORD else r"%s" % string
			self.__manager.emit("search-pattern", pattern)
		except ValueError:
			from gettext import gettext as _
			message = _("ERROR: Search string not found")
			self.__editor.update_message(message, "fail", 10)
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

	def __search_cb(self, manager, string):
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__create_pattern, string.decode("utf-8"), priority=PRIORITY_LOW)
		return False

	def __reset_cb(self, *args):
		self.__search_mode = False
		return False

	def __research_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW as LOW
		self.__timer2 = idle_add(self.__create_pattern, self.__string.decode("utf-8"), priority=LOW)
		return False
