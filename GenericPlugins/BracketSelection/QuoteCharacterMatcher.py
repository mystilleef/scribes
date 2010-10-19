from SCRIBES.SignalConnectionManager import SignalManager

class Matcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "found-open-character", self.__found_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __find_pair_for_character_at(self, open_offset):
		from Exceptions import NoPairCharacterFound
		try:
			iterator = self.__editor.textbuffer.get_iter_at_offset(open_offset)
			open_character = iterator.get_char()
			from Utils import QUOTE_CHARACTERS
			if not (open_character in QUOTE_CHARACTERS): return False
			start, end = self.__get_quote_offsets(open_character)
			self.__manager.emit("select-offsets", (start+1, end-1))
		except NoPairCharacterFound:
			self.__manager.emit("find-open-character", open_offset)
		return False

	def __get_quote_offsets(self, character):
		from Utils import DOUBLE_QOUTE_RE, SINGLE_QUOTE_RE
		RE = DOUBLE_QOUTE_RE if character == '"' else SINGLE_QUOTE_RE
		iterator = RE.finditer(self.__editor.text.decode("utf-8"))
		offsets = [match.span() for match in iterator]
		offsets = [offset for offset in offsets if self.__cursor_is_inside(offset)]
		from Exceptions import NoPairCharacterFound
		if not offsets: raise NoPairCharacterFound
		return offsets[0]

	def __cursor_is_inside(self, offsets):
		start, end = offsets
		cursor = self.__editor.cursor.get_offset()
		return start < cursor < end

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __found_cb(self, manager, open_offset):
		from gobject import idle_add
		idle_add(self.__find_pair_for_character_at, open_offset)
		return False
