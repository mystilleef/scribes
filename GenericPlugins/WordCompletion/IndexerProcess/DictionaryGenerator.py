class Generator(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("clipboard-text", self.__text_cb)
		manager.connect("index", self.__index_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__clipboard_text = ""
		from re import UNICODE, compile
		self.__pattern = compile(r"[^-\w]", UNICODE)
		from dbus import Dictionary, String, Int32
		try:
			self.__empty_dict = Dictionary({}, signature="ss")
		except:
			self.__empty_dict = Dictionary({}, key_type=String, value_type=Int32)
		return

	def __index(self, text):
		try:
			text = text + self.__clipboard_text
			if not text: raise ValueError
			words = self.__get_words(text)
			if not words: raise ValueError
			dictionary = self.__make_dictionary(words)
			if not dictionary: raise ValueError
			self.__manager.emit("finished", dictionary)
		except ValueError:
			self.__manager.emit("finished", self.__empty_dict)
		return False

	def __get_words(self, text):
		from re import split
		self.__manager.response()
		words = split(self.__pattern, text)
		self.__manager.response()
		words = [word for word in words if self.__filter(word)]
		return words

	def __filter(self, word):
		self.__manager.response()
		if len(word) < 4: return False
		self.__manager.response()
		if word.startswith("---"): return False
		self.__manager.response()
		if word.startswith("___"): return False
		self.__manager.response()
		return True

	def __make_dictionary(self, words):
		dictionary = {}
		for string in words:
			self.__manager.response()
			if string in dictionary.keys():
				dictionary[string] += 1
			else:
				dictionary[string] = 1
		return dictionary

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __index_cb(self, manager, texts):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__index, texts, priority=PRIORITY_LOW)
		return False

	def __text_cb(self, manager, text):
		self.__clipboard_text = text
		return False
