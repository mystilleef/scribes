from SCRIBES.SignalConnectionManager import SignalManager

class Reseter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "execute", self.__execute_cb)
		self.connect(manager, "bounds", self.__bounds_cb)
		self.connect(manager, "win", self.__win_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__bounds = None
		self.__cursor_line = 0
		self.__cursor_index = 0
		return

	def __mark_cursor_position(self):
		self.__cursor_line = self.__editor.cursor.get_line()
		self.__cursor_index = self.__editor.cursor.get_line_index()
		return False

	def __get_iterator_from_line(self, selection_iterator, is_start):
		line = self.__cursor_line if is_start else selection_iterator.get_line()
		number_of_lines = self.__buffer.get_line_count()
		if line > number_of_lines: return self.__buffer.get_bounds()[-1]
		return self.__buffer.get_iter_at_line(line)

	def __get_cursor_index(self, iterator, selection_iterator, is_start):
		index = self.__cursor_index if is_start else selection_iterator.get_line_index()
		line_index = iterator.get_bytes_in_line()
		return line_index if index > line_index else index

	def __restore(self):
		from Utils import get_iter
		selection_iterator = get_iter(self.__bounds, self.__buffer)[0]
		is_start = selection_iterator.is_start()
		iterator = self.__get_iterator_from_line(selection_iterator, is_start)
		index = self.__get_cursor_index(iterator, selection_iterator, is_start)
		iterator.set_line_index(index)
		self.__buffer.place_cursor(iterator)
		if is_start: self.__editor.move_view_to_cursor(True)
		self.__manager.emit("restored-cursor-position")
		return False

	def __execute_cb(self, *args):
		self.__mark_cursor_position()
		return False

	def __win_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__restore)
		return False

	def __bounds_cb(self, manager, bounds):
		self.__bounds = bounds
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
