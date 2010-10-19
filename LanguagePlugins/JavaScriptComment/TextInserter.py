from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "comment-boundary", self.__boundary_cb)
		self.connect(manager, "processed-text", self.__text_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__boundaries = ()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __insert(self, text):
		start, end = self.__get_iters_from(self.__boundaries)
		self.__buffer.begin_user_action()
		self.__buffer.delete(start, end) 
		self.__buffer.insert_at_cursor(text)
		self.__buffer.end_user_action()
		self.__manager.emit("inserted-text")
		return False

	def __get_iters_from(self, boundaries):
		start = self.__buffer.get_iter_at_mark(boundaries[0])
		end = self.__buffer.get_iter_at_mark(boundaries[1])
		return start, end

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundaries):
		self.__boundaries = boundaries
		return False

	def __text_cb(self, manager, text):
		from gobject import idle_add
		idle_add(self.__insert, text)
		return False
