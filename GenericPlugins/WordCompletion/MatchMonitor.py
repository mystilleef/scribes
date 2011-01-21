from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__sigid1 = self.connect(manager, "invalid-string", self.__invalid_cb)
		self.__sigid2 = self.connect(manager, "valid-string", self.__valid_cb)
		self.connect(manager, "dictionary", self.__dictionary_cb)
		self.connect(manager, "enable-word-completion", self.__completion_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__found = False
		self.__blocked = False
		self.__dictionary = {}
		return False

	def __destroy(self):
		del self.__dictionary
		self.disconnect()
		del self
		return False

	def __process(self, string):
		matches = self.__find_matches(string)
		self.__emit_matches(matches) if matches else self.__emit_no_matches()
		return False

	def __get_match_list(self, word):
		match_list = []
		dictionary = self.__dictionary
		for items in dictionary.items():
			if not (items[0].startswith(word) and (items[0] != word)): continue
			match_list.append(list(items))
		return match_list

	def __get_matches(self, match_list):
		matches = []
		for items in match_list:
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
		if (x[1] < y[1]): return 1
		if (x[1] > y[1]): return -1
		return 0

	def __emit_matches(self, matches):
		self.__found = True
		self.__manager.emit("match-found", matches)
		return False

	def __emit_no_matches(self):
		if self.__found is False: return False
		self.__manager.emit("no-match-found")
		self.__found = False
		return False

	def __block(self):
		if self.__blocked: return False
		self.__manager.handler_block(self.__sigid1)
		self.__manager.handler_block(self.__sigid2)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__manager.handler_unblock(self.__sigid1)
		self.__manager.handler_unblock(self.__sigid2)
		self.__blocked = False
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __invalid_cb(self, *args):
		self.__emit_no_matches()
		return False

	def __valid_cb(self, manager, string):
		self.__process(string)
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False

	def __completion_cb(self, manager, enable_word_completion):
		self.__unblock() if enable_word_completion else self.__block()
		return False
