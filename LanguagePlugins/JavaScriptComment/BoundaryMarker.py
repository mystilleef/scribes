from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		from MultiCommentSearcher import Searcher
		self.__searcher = Searcher()
		iterator_copy = self.__editor.cursor.copy
		self.__lmark = self.__editor.create_left_mark(iterator_copy())
		self.__rmark = self.__editor.create_right_mark(iterator_copy())
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.delete_mark(self.__lmark)
		self.__editor.delete_mark(self.__rmark)
		del self
		return False

	def __mark_region(self, start, end):
		self.__buffer.move_mark(self.__lmark, start)
		self.__buffer.move_mark(self.__rmark, end)
		return

	def __mark_comment_region(self):
		from Exceptions import NoMultiCommentCharacterError
		try:
			text = self.__editor.text
			boundaries = self.__searcher.find_comment_boundaries(text, self.__editor.cursor.get_offset())
			if not boundaries: raise NoMultiCommentCharacterError
			start = self.__buffer.get_iter_at_offset(boundaries[0])
			end = self.__buffer.get_iter_at_offset(boundaries[1])
			self.__mark_region(start, end)
		except NoMultiCommentCharacterError:
			self.__mark_region(*self.__editor.get_line_bounds())
		return

	def __emit(self):
		self.__mark_region(*self.__editor.selection_bounds) if self.__editor.has_selection else self.__mark_comment_region()
		self.__manager.emit("comment-boundary", (self.__lmark, self.__rmark))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__emit)
		return False
