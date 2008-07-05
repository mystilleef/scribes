class Marker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("toggle-bookmark", self.__toggle_bookmark_cb)
		self.__restore_marks()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __set_properties(self):
		pixbuf = self.__create_pixbuf()
		self.__editor.textview.set_mark_category_pixbuf("scribes_bookmark", pixbuf)
		self.__editor.textview.set_mark_category_priority("scribes_bookmark", 1)
		return

	def __get_line(self, line=None):
		if line is None: return self.__editor.get_cursor_line()
		return line if self.__line_exists(line) else None

	def __create_pixbuf(self):
		from os.path import join
		current_folder = self.__editor.get_current_folder(globals())
		image_file = join(current_folder, "bookmarks.png")
		from gtk import Image
		image = Image()
		image.set_from_file(image_file)
		pixbuf = image.get_pixbuf()
		return pixbuf

	def __toggle_mark(self):
		try:
			self.__unmark() if self.__line_is_marked() else self.__mark()
		except ValueError:
			pass
		return

	def __mark(self, line=None):
		try:
			iterator = self.__iter_at_line(line)
			if iterator is None: raise ValueError
			self.__editor.textbuffer.create_source_mark(None, "scribes_bookmark", iterator)
		except ValueError:
			pass
		return

	def __unmark(self, line=None):
		try:
			iterator = self.__iter_at_line(line)
			if iterator is None: raise ValueError
			end = self.__editor.forward_to_line_end(iterator.copy())
			self.__editor.textbuffer.remove_source_marks(iterator, end, "scribes_bookmark")
		except ValueError:
			pass
		return

	def __remove_all_marks(self, lines):
		if not lines: return
		unmark = self.__unmark
		[unmark(line) for line in lines]
		return

	def __restore_marks(self):
		uri = self.__editor.uri
		if uri in (None, ""): return
		from Metadata import get_value
		lines = get_value(uri)
		if not lines: return
		mark = self.__mark
		[mark(line) for line in lines]
		return

	def __iter_at_line(self, line=None):
		get_iter = self.__editor.textbuffer.get_iter_at_line
		if line: return get_iter(line) if self.__line_exists(line) else None
		return get_iter(self.__editor.get_cursor_line())

	def __line_exists(self, line):
		iterator = self.__editor.textbuffer.get_bounds()[1]
		if line > iterator.get_line(): return False
		return True

	def __line_is_marked(self, line=None):
		line = self.__get_line()
		if line is None: raise ValueError
		marks = self.__editor.textbuffer.get_source_marks_at_line(line, "scribes_bookmark")
		if marks: return True
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggle_bookmark_cb(self, *args):
		self.__toggle_mark()
		return False
