from SCRIBES.SignalConnectionManager import SignalManager

class Matcher(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "found-open-character", self.__found_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __find_pair_for_character_at(self, open_offset):
		from Exceptions import NoPairCharacterFound
		try:
			iterator = self.__editor.textbuffer.get_iter_at_offset(open_offset)
			open_character = iterator.get_char()
			from Utils import QUOTE_CHARACTERS
			if open_character in QUOTE_CHARACTERS: return False
			pair_iterator = self.__editor.find_matching_bracket(iterator.copy())
			if not pair_iterator: raise NoPairCharacterFound
			close_offset = pair_iterator.get_offset()
			self.__manager.emit("check-pair-range", (open_offset+1, close_offset))
		except NoPairCharacterFound:
			self.__manager.emit("find-open-character", open_offset)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __found_cb(self, manager, offset):
		from gobject import idle_add
		idle_add(self.__find_pair_for_character_at, offset)
		return False
