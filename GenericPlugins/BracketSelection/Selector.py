from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "select-offsets", self.__select_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __select(self, offsets):
		get_iter = self.__editor.textbuffer.get_iter_at_offset
		start, end = get_iter(offsets[0]), get_iter(offsets[1])
		self.__editor.response()
		self.__editor.textbuffer.select_range(start, end)
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __select_cb(self, manager, offsets):
		from gobject import idle_add
		idle_add(self.__select, offsets)
		return False
