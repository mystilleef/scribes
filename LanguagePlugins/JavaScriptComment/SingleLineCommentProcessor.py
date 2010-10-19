from SCRIBES.SignalConnectionManager import SignalManager

class Processor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "single-line-boundary", self.__boundary_cb)

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
		text = self.__extract_text_from(boundaries)
		from Utils import has_comment
		text = self.__uncomment(text) if has_comment(text) else self.__comment(text)
		self.__manager.emit("processed-text", text)
		return False

	def __uncomment(self, text):
		self.__manager.emit("commenting", False)
		from Utils import uncomment
		return uncomment(text)

	def __comment(self, text):
		self.__manager.emit("commenting", True)
		from Utils import comment
		return comment(text)

	def __extract_text_from(self, boundaries):
		start = self.__buffer.get_iter_at_mark(boundaries[0])
		end = self.__buffer.get_iter_at_mark(boundaries[1])
		return self.__buffer.get_text(start, end)

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundaries):
		from gobject import idle_add
		idle_add(self.__emit, boundaries)
		return False
