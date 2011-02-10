from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Feedback(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "activate", self.__row_cb)
		self.connect(manager, "search-pattern", self.__search_cb)
		self.connect(manager, "filtered-data", self.__data_cb)
		self.connect(manager, "selected-row", self.__row_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__pattern = ""
		self.__matches = 0
		return

	def __update_message(self, data, time):
		self.__manager.emit("message", data)
		self.__hide_after(time)
		return False

	def __hide(self):
		self.__manager.emit("hide-message")
		return False

	def __hide_after(self, time):
		self.__remove_all_timers()
		from gobject import timeout_add
		self.__timer1 = timeout_add(time*1000, self.__hide)
		return False

	def __set_message(self):
		if not self.__pattern:
			message = _("%s files") if self.__matches else _("No files")
			if self.__matches == 1: message = _("%s file")
		else:
			message = _("%s matches found") if self.__matches else _("No match found")
			if self.__matches == 1: message = _("%s match found")
		time = 10
		message_type = "INFO" if self.__matches else "ERROR"
		message = message % str(self.__matches) if self.__matches else message
		data = (message_type, message)
		self.__update_message(data, time)
		return False

	def __search_message(self):
		data = ("PROGRESS", _("Searching please wait..."))
		self.__update_message(data, 21)
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

	def __search_cb(self, manager, pattern):
		self.__pattern = pattern
		self.__remove_all_timers()
		from gobject import timeout_add
		self.__timer2 = timeout_add(250, self.__search_message, priority=9999)
		return False

	def __data_cb(self, manager, data):
		self.__matches = len(data)
		return False

	def __row_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add
		idle_add(self.__set_message, priority=9999)
		return False
