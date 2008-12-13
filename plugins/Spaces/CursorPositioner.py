class Positioner(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("line-offset", self.__offset_cb)
		self.__sigid3 = manager.connect("inserted-text", self.__inserted_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__data = None
		self.__old_text = None
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __get_text_on_line(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line)
		start = self.__editor.backward_to_line_begin(iterator.copy())
		end = self.__editor.forward_to_line_end(start.copy())
		text = self.__editor.textbuffer.get_text(start, end)
		return text

	def __position(self):
		line, offset = self.__data
		new_text = self.__get_text_on_line(line)
		new_offset = offset + (len(new_text) - len(self.__old_text))
		get_iter = self.__editor.textbuffer.get_iter_at_line_offset
		iterator = get_iter(line, new_offset)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor(True)
		self.__data = None
		self.__old_text = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __offset_cb(self, manager, data):
		self.__data = data
		self.__old_text = self.__get_text_on_line(data[0])
		return False

	def __inserted_cb(self, *args):
		self.__position()
		return False
