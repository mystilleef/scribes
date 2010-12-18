from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "exit-sparkup-mode", self.__exit_cb)
		self.connect(manager, "removed-placeholders", self.__moved_cb, True)
		self.connect(manager, "placeholder-marks", self.__marks_cb, True)
		self.__sigid1 = self.connect(editor, "cursor-moved", self.__moved_cb, True)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__nesting_level = 0
		self.__marks = {}
		self.__current_placeholder = ()
		self.__blocked = False
		return

	def __check(self):
		if self.__in_range(self.__current_placeholder): return False
		current_placeholder = self.__get_current_placeholder()
		if current_placeholder == self.__current_placeholder: return False
		self.__current_placeholder = current_placeholder
		self.__manager.emit("cursor-in-placeholder", current_placeholder)
		return False

	def __get_current_placeholder(self):
		marks = self.__marks[self.__nesting_level]
		current_placeholder = ()
		for placeholder in marks:
			if not self.__in_range(placeholder): continue
			current_placeholder = placeholder
			break
		return current_placeholder

	def __in_range(self, marks):
		if not marks: return False
		go = self.__get_offset
		smark, emark = marks
		offset = self.__editor.cursor.get_offset()
		if go(smark) <= offset <= go(emark): return True
		return False

	def __get_offset(self, mark):
		return self.__buffer.get_iter_at_mark(mark).get_offset()

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

	def __marks_cb(self, manager, marks):
		self.__nesting_level += 1
		self.__marks[self.__nesting_level] = marks
		self.__current_placeholder = ()
		self.__unblock()
		return False

	def __exit_cb(self, *args):
		del self.__marks[self.__nesting_level]
		self.__nesting_level -= 1
		if self.__nesting_level < 0: self.__nesting_level = 0
		self.__current_placeholder = ()
		self.__check() if self.__nesting_level else self.__block()
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
