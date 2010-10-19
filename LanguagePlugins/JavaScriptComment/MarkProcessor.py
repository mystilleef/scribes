from SCRIBES.SignalConnectionManager import SignalManager

class Processor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "comment-boundary", self.__boundary_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __emit(self, boundaries):
		signal = "single-line-boundary" if self.__on_same_line(boundaries) else "multiline-boundary"
		if signal == "multiline-boundary": self.__move_to_edge(boundaries)
		self.__manager.emit(signal, boundaries)
		return False

	def __on_same_line(self, boundaries):
		start_line = self.__buffer.get_iter_at_mark(boundaries[0]).get_line()
		end_line = self.__buffer.get_iter_at_mark(boundaries[1]).get_line()
		return start_line == end_line

	def __move_to_edge(self, boundaries):
		# Move left mark to start of line.
		start = self.__buffer.get_iter_at_mark(boundaries[0])
		start = self.__editor.backward_to_line_begin(start)
		self.__buffer.move_mark(boundaries[0], start)
		# Move right mark to end of line.
		end = self.__buffer.get_iter_at_mark(boundaries[1])
		end = self.__editor.forward_to_line_end(end)
		self.__buffer.move_mark(boundaries[1], end)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundaries):
		from gobject import idle_add
		idle_add(self.__emit, boundaries)
		return False
