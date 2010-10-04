from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __check(self):
		from Exceptions import NoSelectionFound, NoPairCharacterFound
		try:
			if self.__editor.has_selection is False: raise NoSelectionFound
			boundaries = self.__editor.selection_bounds
			if self.__inside_pair_characters(boundaries) is False: raise NoPairCharacterFound
			self.__select(boundaries)
		except (NoSelectionFound, NoPairCharacterFound):
			self.__manager.emit("find-open-character", self.__editor.cursor.get_offset())
		return False

	def __inside_pair_characters(self, boundaries):
		start, end = boundaries[0].copy(), boundaries[1].copy()
		if not start.backward_char(): return False
		from Utils import get_pair_for
		close_character = get_pair_for(start.get_char())
		if not close_character: return False
		if close_character != end.get_char(): return False
		return True

	def __select(self, boundaries):
		start, end = boundaries[0].copy(), boundaries[1].copy()
		start.backward_char()
		end.forward_char()
		start_offset, end_offset = start.get_offset(), end.get_offset()
		self.__manager.emit("select-offsets", (start_offset, end_offset))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__check)
		return False
