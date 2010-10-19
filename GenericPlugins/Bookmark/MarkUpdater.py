from SCRIBES.SignalConnectionManager import SignalManager
from Utils import BOOKMARK_NAME

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor.textbuffer, "source-mark-updated", self.__updated_cb, True)
		self.connect(editor, "modified-file", self.__modified_cb, True)
		self.connect(editor, "renamed-file", self.__updated_cb, True)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__lines = ()
		return

	def __destroy(self):
		self.__update()
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __line_from(self, mark):
		iter_at_mark = self.__buffer.get_iter_at_mark
		return iter_at_mark(mark).get_line()

	def __get_bookmarked_lines(self):
		mark = self.__find_first_mark()
		marks = self.__get_all_marks(mark)
		lines = [self.__line_from(mark) for mark in marks]
		return tuple(lines)

	def __find_first_mark(self):
		iterator = self.__buffer.get_bounds()[0]
		marks = self.__buffer.get_source_marks_at_iter(iterator, BOOKMARK_NAME)
		if marks: return marks[0]
		found_mark = self.__buffer.forward_iter_to_source_mark(iterator, BOOKMARK_NAME)
		if found_mark is False: raise ValueError
		marks = self.__buffer.get_source_marks_at_iter(iterator, BOOKMARK_NAME)
		return marks[0]

	def __get_all_marks(self, mark):
		marks = []
		append = marks.append
		append(mark)
		while True:
			mark = mark.next(BOOKMARK_NAME)
			if mark is None: break
			append(mark)
		return marks

	def __update(self):
		try:
			lines = self.__get_bookmarked_lines()
		except ValueError:
			lines = ()
		finally:
			if lines == self.__lines: return False
			self.__lines = lines
			self.__manager.emit("lines", lines)
		return False

	def __optimize(self):
		methods = (
			self.__update, self.__get_bookmarked_lines,
			self.__find_first_mark, self.__get_all_marks,
		)
		self.__editor.optimize(methods)
		return False

	def __updated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False

	def __modified_cb(self, editor, modified):
		from gobject import idle_add
		idle_add(self.__update, priority=9999999)
		return False
