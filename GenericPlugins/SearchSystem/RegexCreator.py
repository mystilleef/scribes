from SCRIBES.SignalConnectionManager import SignalManager

class Creator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "new-pattern", self.__pattern_cb)
		self.connect(manager, "match-case-flag", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__ignore_case = False
		return 

	def __regex_object(self, pattern):
		from re import I, U, M, L, error, compile as compile_
		try:
			flags = I|M|U|L if self.__ignore_case else U|M|L
			from gobject import idle_add
			idle_add(self.__manager.emit, "regex-flags", flags)
			regex_object = compile_(pattern, flags)
			idle_add(self.__manager.emit, "new-regex", regex_object)
		except error:
			from gobject import idle_add
			idle_add(self.__manager.emit, "reset")
			idle_add(self.__manager.emit, "search-complete")
			from gettext import gettext as _
			message = _("Error: improperly escaped regular expression")
			self.__editor.update_message(message, "no", 7)
			idle_add(self.__manager.emit, "focus-entry")
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __pattern_cb(self, manager, pattern):
		from gobject import idle_add
		idle_add(self.__regex_object, pattern)
		return False

	def __update_cb(self, manager, match_case):
		self.__ignore_case = not match_case
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
