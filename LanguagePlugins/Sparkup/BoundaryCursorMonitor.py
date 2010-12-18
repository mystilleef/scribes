from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "boundary-marks", self.__marks_cb)
		self.connect(manager, "exit-sparkup-mode", self.__exit_cb)
		self.__sigid1 = self.connect(editor, "cursor-moved", self.__moved_cb, True)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__nesting_level = 0
		self.__blocked = False
		self.__boundaries = {}
		return

	def __check(self):
		cursor_offset = self.__editor.cursor.get_offset()
		start_mark, end_mark = self.__boundaries[self.__nesting_level]
		go = lambda mark: self.__buffer.get_iter_at_mark(mark).get_offset()
		start_offset, end_offset = go(start_mark), go(end_mark)
		if start_offset <= cursor_offset <= end_offset: return False
		self.__manager.emit("exit-sparkup-mode")
		return False

	def __block(self):
		if self.__blocked: return False
		self.__editor.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__editor.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __marks_cb(self, manager, boundaries):
		self.__nesting_level += 1
		self.__boundaries[self.__nesting_level] = boundaries
		self.__unblock()
		return False

	def __exit_cb(self, *args):
		del self.__boundaries[self.__nesting_level]
		self.__nesting_level -= 1
		if self.__nesting_level < 0: self.__nesting_level = 0
		if self.__nesting_level: return False
		self.__block()
		return False

	def __moved_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__check, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
