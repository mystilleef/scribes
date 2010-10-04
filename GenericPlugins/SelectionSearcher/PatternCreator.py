from SCRIBES.SignalConnectionManager import SignalManager
MATCH_WORD = True

class Creator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "search", self.__search_cb)
		self.connect(manager, "research", self.__research_cb)
		self.connect(manager, "reset", self.__reset_cb)
		editor.response()

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
			message = _("ERROR: Search string not found") 
			self.__editor.update_message(message, "fail", 10)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __search_cb(self, manager, string):
		from gobject import idle_add
		idle_add(self.__create_pattern, string.decode("utf-8"), priority=9999)
		return False

	def __reset_cb(self, *args):
		self.__search_mode = False
		return False

	def __research_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__create_pattern, self.__string.decode("utf-8"), priority=9999)
		return False
