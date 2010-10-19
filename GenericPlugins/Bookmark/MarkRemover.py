from SCRIBES.SignalConnectionManager import SignalManager

class Remover(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "remove", self.__remove_cb)
		self.connect(manager, "remove-all", self.__remove_all_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __get_region(self, line=None):
		if line is None: return self.__editor.textbuffer.get_bounds()
		start = self.__editor.textbuffer.get_iter_at_line(line)
		end = self.__editor.forward_to_line_end(start.copy())
		return start, end

	def __unmark(self, region):
		start, end = region
		from Utils import BOOKMARK_NAME
		self.__editor.textbuffer.remove_source_marks(start, end, BOOKMARK_NAME)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __remove_cb(self, manager, line):
		from gobject import idle_add
		idle_add(self.__unmark, self.__get_region(line))
		return False
	
	def __remove_all_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__unmark, self.__get_region())
		return False
