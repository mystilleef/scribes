from SCRIBES.SignalConnectionManager import SignalManager

class Searcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "find-open-character", self.__find_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __search_from(self, offset):
		from Exceptions import NoPairCharacterFound
		try:
			search_iterator = self.__editor.textbuffer.get_iter_at_offset(offset)
			character = self.__get_backward_character(search_iterator)
			from Utils import is_open_pair, get_pair_for
			# Search backward for open pair character.
			while is_open_pair(character) is False:
				character = self.__get_backward_character(search_iterator)
			self.__manager.emit("found-open-character", search_iterator.get_offset())
		except NoPairCharacterFound:
			self.__manager.emit("no-pair-character-found")
		return False

	def __get_backward_character(self, search_iterator):
		from Exceptions import NoPairCharacterFound
		result = search_iterator.backward_char()
		if result is False: raise NoPairCharacterFound
		character = search_iterator.get_char()
		return character

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __find_cb(self, manager, offset):
		from gobject import idle_add
		idle_add(self.__search_from, offset)
		return False
