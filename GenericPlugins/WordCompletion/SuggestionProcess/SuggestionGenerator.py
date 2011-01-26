from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "string", self.__string_cb)
		self.connect(manager, "dictionary", self.__dictionary_cb)
		manager.set_data("WordCompletionSuggestions", [])

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__dictionary = {}
		return False

	def __get_suggestions_from(self, string):
		matches = self.__find_matches(string)
		self.__manager.set_data("WordCompletionSuggestions", matches)
		return False

	def __find_matches(self, word):
		dictionary = self.__dictionary
		if not dictionary: return []
		starts_word = lambda string: (string != word) and string.startswith(word)
		matches = [list(items) for items in dictionary.items() if starts_word(items[0])]
		if not matches: return []
		matches.sort(self.__sort)
		return [items[0] for items in matches]

	def __sort(self, x, y):
		if (x[1] < y[1]): return 1
		if (x[1] > y[1]): return -1
		return 0

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __string_cb(self, manager, string):
#		self.__remove_timer()
#		from gobject import idle_add, PRIORITY_HIGH __get_suggestions_from
#		self.__timer = idle_add(self.__get_suggestions_from, string, priority=PRIORITY_HIGH)
		self.__get_suggestions_from(string)
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False
