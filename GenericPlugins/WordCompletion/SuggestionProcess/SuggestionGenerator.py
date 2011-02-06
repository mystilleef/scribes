from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "string", self.__string_cb)
		self.connect(manager, "dictionary", self.__dictionary_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__dictionary = {}
		self.__triggers = ()
		return False

	def __get_suggestions_from(self, string):
		suggestions = self.__find_matches(string)
		self.__manager.set_data("WordCompletionSuggestions", suggestions)
		return False

	def __find_matches(self, word):
		starts_word = lambda string: (string != word) and string.startswith(word)
		matches = (items for items in self.__dictionary.items() if starts_word(items[0]))
		return [items[0] for items in sorted(matches, self.__sort)]

	def __sort(self, x, y):
		if (x[1] < y[1]): return 1
		if (x[1] > y[1]): return -1
		return 0

	def __string_cb(self, manager, string):
		self.__get_suggestions_from(string)
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False
