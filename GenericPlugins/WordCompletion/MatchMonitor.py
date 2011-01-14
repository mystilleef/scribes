from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "invalid-string", self.__invalid_cb)
		self.connect(manager, "valid-string", self.__valid_cb)
		self.connect(manager, "dictionary", self.__dictionary_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__found = False
		self.__dictionary = {}
		return False

	def __destroy(self):
		del self.__dictionary
		self.disconnect()
		del self
		return False

	def __process(self, string):
		self.__editor.refresh()
		matches = self.__find_matches(string)
		self.__emit_matches(matches) if matches else self.__emit_no_matches()
		return False

	def __get_match_list(self, word):
		match_list = []
		dictionary = self.__dictionary
		for items in dictionary.items():
			self.__editor.refresh(False)
			if not (items[0].startswith(word) and (items[0] != word)): continue
			match_list.append(list(items))
			self.__editor.refresh(False)
		return match_list

	def __get_matches(self, match_list):
		matches = []
		for items in match_list:
			self.__editor.refresh(False)
			matches.append(items[0])
			self.__editor.refresh(False)
		return matches

	def __find_matches(self, word):
		self.__editor.refresh(False)
		dictionary = self.__dictionary
		if not dictionary: return None
		match_list = self.__get_match_list(word)
		if not match_list: return None
		match_list.sort(self.__sort)
		return self.__get_matches(match_list)

	def __sort(self, x, y):
		self.__editor.refresh(False)
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
