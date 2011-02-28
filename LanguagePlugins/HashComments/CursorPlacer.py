from SCRIBES.SignalConnectionManager import SignalManager

class Placer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "inserted-text", self.__text_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__cursor_line_offset = 0
		self.__has_selection = False
		return

	def __place(self):
		if self.__has_selection: return False
		start, end = self.__editor.line_bounds
		start_offset, end_offset = start.get_line_offset(), end.get_line_offset()
		cursor_offset = self.__cursor_line_offset
		if cursor_offset < start_offset: cursor_offset = start_offset
		if cursor_offset > end_offset: cursor_offset = end_offset
		iterator = self.__editor.cursor.copy()
		iterator.set_line_offset(cursor_offset)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.grab_focus()
		from gobject import idle_add
		idle_add(self.__manager.emit, "finished")
		return False

	def __text_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__place)
		return False

	def __activate_cb(self, *args):
		self.__has_selection = self.__editor.has_selection
		self.__cursor_line_offset = self.__editor.cursor.get_line_offset()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
