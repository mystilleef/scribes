from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "bounds", self.__bounds_cb)
		self.connect(manager, "result", self.__result_cb)
		self.connect(manager, "output-mode", self.__output_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bounds = None
		self.__output_mode = "replace"
		return

	def __insert(self, text):
		_buffer = self.__editor.textbuffer
		_buffer.begin_user_action()
		from Utils import get_iter
		_buffer.delete(*get_iter(self.__bounds, _buffer))
		_buffer.insert_at_cursor(text)
		_buffer.end_user_action()
		self.__manager.emit("win")
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __bounds_cb(self, manager, bounds):
		self.__bounds = bounds
		return False

	def __result_cb(self, manager, text):
		if self.__output_mode != "replace": return False
		from gobject import idle_add
		idle_add(self.__insert, text)
		return False

	def __output_cb(self, manager, output):
		self.__output_mode = output
		return False
