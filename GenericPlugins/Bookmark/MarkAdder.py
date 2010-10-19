from SCRIBES.SignalConnectionManager import SignalManager

class Adder(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "add", self.__add_cb)
		self.connect(manager, "bookmark-lines", self.__lines_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __mark(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line)
		from Utils import BOOKMARK_NAME
		self.__editor.textbuffer.create_source_mark(None, BOOKMARK_NAME, iterator)
		return False

	def __update(self, lines):
		[self.__mark(line) for line in lines]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, manager, line):
		from gobject import idle_add
		idle_add(self.__mark, line)
		return False

	def __lines_cb(self, manager, lines):
		from gobject import idle_add
		idle_add(self.__update, lines)
		return False
