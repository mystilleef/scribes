from SCRIBES.SignalConnectionManager import SignalManager

class Navigator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "column-edit-point", self.__point_cb)
		self.connect(manager, "deactivate", self.__clear_cb)
		self.connect(manager, "activate", self.__clear_cb)
		self.connect(manager, "inserted-text", self.__clear_cb)
		self.connect(manager, "clear", self.__clear_cb)
		self.connect(manager, "column-mode-reset", self.__clear_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__cursor_offset = None
		self.__direction = None
		self.__start_line = None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __toggle_edit_point(self, direction):
		self.__editor.response()
		if self.__direction is None: self.__direction = direction
		if self.__direction != direction: self.__update_direction(direction)
		cursor = self.__editor.cursor
		cursor_offset = cursor.get_line_offset()
		if self.__start_line is None: self.__start_line = cursor.get_line()
		if self.__cursor_offset is None: self.__update_offset(cursor_offset)
		result = cursor.forward_line() if direction == "down" else cursor.backward_line()
		if result is False: return False
		iterator = self.__editor.forward_to_line_end(cursor)
		offset = iterator.get_line_offset()
		offset = offset if self.__cursor_offset > offset else self.__cursor_offset
		iterator.set_line_offset(offset)
		self.__buffer.place_cursor(iterator)
		self.__view.scroll_mark_onscreen(self.__buffer.get_insert())
		if iterator.get_line() == self.__start_line: return False
		self.__manager.emit("toggle-edit-point")
		self.__editor.response()
		return False

	def __update_offset(self, cursor_offset):
		self.__editor.response()
		self.__cursor_offset = cursor_offset
		self.__manager.emit("add-edit-point")
		self.__editor.response()
		return False

	def __update_direction(self, direction):
		self.__editor.response()
		self.__direction = direction
		self.__manager.emit("toggle-edit-point")
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __point_cb(self, manager, direction):
		self.__toggle_edit_point(direction)
		return False

	def __clear_cb(self, *args):
		self.__cursor_offset = None
		self.__direction = None
		self.__start_line = None
		return False
