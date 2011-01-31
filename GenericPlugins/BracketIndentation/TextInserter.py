from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "insert", self.__insert_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__lmark, self.__rmark = manager.get_data("BracketRegionMarks")
		return

	def __insert(self, string):
		start = self.__buffer.get_iter_at_mark(self.__lmark)
		end = self.__buffer.get_iter_at_mark(self.__rmark)
		self.__buffer.begin_user_action()
		self.__buffer.delete(start, end)
		self.__buffer.insert_at_cursor(string)
		iterator = self.__editor.cursor
		iterator.backward_line()
		iterator.forward_to_line_end()
		self.__buffer.place_cursor(iterator)
		self.__view.scroll_mark_onscreen(self.__rmark)
		self.__buffer.end_user_action()
		self.__manager.emit("done")
		return False

	def __insert_cb(self, manager, string):
		self.__insert(string)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
