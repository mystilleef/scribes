class Creator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("new-pattern", self.__pattern_cb)
		self.__sigid3 = manager.connect("match-case-flag", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__ignore_case = False
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __regex_object(self, pattern):
		from re import I, U, M, compile as compile_
		flags =  I|M|U if self.__ignore_case else M|U
		self.__manager.emit("regex-flags", flags)
		regex_object = compile_(pattern, flags)
		self.__manager.emit("new-regex", regex_object)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __pattern_cb(self, manager, pattern):
		self.__regex_object(pattern)
		return False

	def __update_cb(self, manager, match_case):
		self.__ignore_case = not match_case
		return False
