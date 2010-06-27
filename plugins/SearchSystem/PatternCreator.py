class Creator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search-string", self.__search_string_cb)
		self.__sigid3 = manager.connect("search", self.__search_cb)
		self.__sigid4 = manager.connect("search-mode-flag", self.__search_mode_cb)
		self.__sigid5 = manager.connect("match-word-flag", self.__match_word_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__string = None
		self.__regex_mode = True
		self.__match_word = True
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return

	def __create_pattern(self):
		try:
			if not self.__string: raise AssertionError
			if self.__regex_mode: raise ValueError
			from re import escape
			string = escape(self.__string)
			pattern = r"\b%s\b" % string if self.__match_word else r"%s" % string
		except ValueError:
			pattern = r"%s" % self.__string
		except AssertionError:
			self.__manager.emit("reset")
			message = _("ERROR: Empty search string")
			self.__editor.update_message(message, "fail", 10)
			self.__manager.emit("search-complete")
		finally:
			if self.__string: self.__manager.emit("new-pattern", pattern)
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __search_string_cb(self, manager, string):
		self.__string = string.decode("utf-8")
		return False

	def __search_cb(self, *args):
		self.__create_pattern()
		return False

	def __search_mode_cb(self, manager, search_mode):
		self.__regex_mode = True if search_mode == "regex" else False
		return False

	def __match_word_cb(self, manager, match_word):
		self.__match_word = match_word
		return False
