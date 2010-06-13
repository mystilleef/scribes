from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "single-line-boundary", self.__boundary_cb)
		self.connect(manager, "inserted-text", self.__text_cb)
		self.connect(manager, "commenting", self.__commenting_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__selection = False
		self.__buffer = editor.textbuffer
		self.__offset = 0
		self.__boundaries = ()
		self.__commenting = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __position(self):
		if self.__selection: return False
		if not self.__boundaries: return False
		offset = self.__offset + 2 if self.__commenting else self.__offset - 2
		iterator = self.__buffer.get_iter_at_offset(offset)
		self.__buffer.place_cursor(iterator)
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
		self.__offset = self.__editor.cursor.get_offset()
		return False

	def __text_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__position)
		return False

	def __commenting_cb(self, manager, commenting):
		self.__commenting = commenting
		return False
