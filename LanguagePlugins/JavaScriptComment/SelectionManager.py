from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "multiline-boundary", self.__boundary_cb)
		self.connect(manager, "inserted-text", self.__text_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__selection = False
		self.__buffer = editor.textbuffer
		self.__boundaries = ()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __select_range(self):
		if not (self.__selection or self.__boundaries): return False
		start = self.__buffer.get_iter_at_mark(self.__boundaries[0])
		end = self.__buffer.get_iter_at_mark(self.__boundaries[1])
		self.__buffer.select_range(start, end)
		self.__manager.emit("finished")
		self.__boundaries = ()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundaries):
		self.__boundaries = boundaries
		return False

	def __activate_cb(self, *args):
		self.__selection = self.__editor.has_selection
		return False

	def __text_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__select_range)
		return False
