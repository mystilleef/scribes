class Monitor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("invalid-string", self.__invalid_cb)
		self.__sigid3 = manager.connect("valid-string", self.__valid_cb)
		self.__sigid4 = manager.connect("dictionary", self.__dictionary_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=444)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__found = False
		self.__dictionary = {}
		return False

	def __destroy(self):
		del self.__dictionary
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return False

	def __process(self, string):
		matches = self.__find_matches(string)
		self.__emit_matches(matches) if matches else self.__emit_no_matches()
		return False

	def __get_match_list(self, word):
		match_list = []
		dictionary = self.__dictionary
		for items in dictionary.items():
			self.__editor.response()
			if not (items[0].startswith(word) and (items[0] != word)): continue
			match_list.append(list(items))
		return match_list

	def __get_matches(self, match_list):
		matches = []
		for items in match_list:
			self.__editor.response()
			matches.append(items[0])
		return matches

	def __find_matches(self, word):
		dictionary = self.__dictionary
		if not dictionary: return None
		match_list = self.__get_match_list(word)
		if not match_list: return None
		match_list.sort(self.__sort)
		return self.__get_matches(match_list)

	def __sort(self, x, y):
		self.__editor.response()
		if (x[1] < y[1]): return 1
		if (x[1] > y[1]): return -1
		return 0

	def __precompile_methods(self):
		methods = (self.__find_matches, self.__sort, self.__process)
		self.__editor.optimize(methods)
		return False

	def __emit_matches(self, matches):
		self.__found = True
		self.__manager.emit("match-found", matches)
		return False

	def __emit_no_matches(self):
		if self.__found is False: return False
		self.__manager.emit("no-match-found")
		self.__found = False
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __invalid_cb(self, *args):
		self.__emit_no_matches()
		return False

	def __valid_cb(self, manager, string):
		from gobject import idle_add
		idle_add(self.__process, string)
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False
