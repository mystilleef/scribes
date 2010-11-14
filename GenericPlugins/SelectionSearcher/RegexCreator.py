from SCRIBES.SignalConnectionManager import SignalManager
IGNORE_CASE = False

class Creator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "search-pattern", self.__pattern_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 

	def __destroy(self):
		self.disconnect()
		del self
		return 

	def __regex_object(self, pattern):
		from re import I, U, M, L, compile as compile_
		flags = I|M|U|L if IGNORE_CASE else U|M|L
		regex_object = compile_(pattern, flags)
		self.__manager.emit("regex-object", regex_object)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __pattern_cb(self, manager, pattern):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__regex_object, pattern, priority=PRIORITY_LOW)
		return False
