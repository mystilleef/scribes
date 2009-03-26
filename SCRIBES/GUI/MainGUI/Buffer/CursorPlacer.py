class Placer(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("loaded-file", self.__loaded_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __place(self):
		self.__editor.response()
		line, index = self.__get_cursor_data()
		iterator = self.__get_cursor_iterator(line)
		index = self.__get_cursor_index(iterator, index)
		iterator.set_line_index(index)
		self.__buffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor(True)
		self.__editor.response()
		return False

	def __get_cursor_data(self):
		from SCRIBES.CursorMetadata import get_value
		position = get_value(self.__editor.uri)
		return position[0] + 1, position[1]

	def __get_cursor_iterator(self, line):
		number_of_lines = self.__buffer.get_line_count()
		if line > number_of_lines: return self.__buffer.get_start_iter()
		return self.__buffer.get_iter_at_line(line - 1)

	def __get_cursor_index(self, iterator, index):
		line_index = iterator.get_bytes_in_line()
		return line_index if index > line_index else index

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __loaded_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__place, priority=9999)
		return False
