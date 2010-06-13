from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

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
		self.__buffer = editor.textbuffer
		from MultiCommentSearcher import Searcher
		self.__searcher = Searcher()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __mark_region(self, start, end):
		lmark = self.__editor.create_left_mark(start)
		rmark = self.__editor.create_right_mark(end)
		return lmark, rmark

	def __mark_comment_region(self):
		from Exceptions import NoMultiCommentCharacterError
		try:
			text = self.__editor.text
			boundaries = self.__searcher.find_comment_boundaries(text, self.__editor.cursor.get_offset())
			if not boundaries: raise NoMultiCommentCharacterError
			start = self.__buffer.get_iter_at_offset(boundaries[0])
			end = self.__buffer.get_iter_at_offset(boundaries[1])
			lmark, rmark = self.__mark_region(start, end)
		except NoMultiCommentCharacterError:
			lmark, rmark = self.__mark_region(*self.__editor.get_line_bounds())
		return lmark, rmark

	def __emit(self):
		marks = self.__mark_region(*self.__editor.selection_bounds) if self.__editor.has_selection else self.__mark_comment_region()
		self.__manager.emit("comment-boundary", marks)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__emit)
		return False
