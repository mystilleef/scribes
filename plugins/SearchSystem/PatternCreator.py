class Creator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search-string", self.__search_string_cb)
		self.__sigid3 = manager.connect("search", self.__search_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__string = None
		self.__regex_mode = False
		self.__match_word = True
		return False
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __create_pattern(self):
		try:
			if self.__regex_mode: raise ValueError
			from re import escape
			pattern = escape(self.__string)
			if self.__match_word: pattern = r"\b" + pattern + r"\b"
		except ValueError:
			pattern = copy(self.__string)
		finally:
			self.__manager.emit("new-pattern", pattern)
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __search_string_cb(self, manager, string):
		self.__string = string
		return False
	
	def __search_cb(self, *args):
		self.__create_pattern()
		return False
