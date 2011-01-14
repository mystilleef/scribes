from SCRIBES.SignalConnectionManager import SignalManager

class Requester(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__sigid1 = self.connect(editor, "cursor-moved", self.__moved_cb, True)
		self.__sigid2 = self.connect(self.__view, "key-press-event", self.__event_cb)
		self.connect(self.__buffer, "changed", self.__changed_cb, True)
		self.connect(self.__buffer, "insert-text", self.__insert_cb, True)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__view = editor.textview
		self.__blocked = False
		self.__line_number = 0
		return

	def __index(self):
		self.__manager.emit("index")
		return False

	def __index_async(self):
		self.__remove_timer(1)
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__index, priority=PRIORITY_LOW)
		if self.__blocked is False: self.__block()
		return False

	def __check_line(self):
		line_number = self.__editor.cursor.get_line()
		if line_number == self.__line_number: return False
		self.__line_number = line_number
		self.__index_async()
		return False

	def __block(self):
		if self.__blocked: return False
		self.__editor.handler_block(self.__sigid1)
		self.__view.handler_block(self.__sigid2)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__editor.handler_unblock(self.__sigid1)
		self.__view.handler_unblock(self.__sigid2)
		self.__blocked = False
		return False

	def __remove_timer(self, timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[timer])
		except AttributeError:
			pass
		return False

	def __insert_cb(self, textbuffer, iterator, text, length):
		if text.isalnum(): return False
		self.__index_async()
		return False

	def __changed_cb(self, *args):
		if self.__blocked: self.__unblock()
		return False

	def __moved_cb(self, *args):
		self.__remove_timer(2)
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__check_line, priority=PRIORITY_LOW)
		return False

	def __event_cb(self, textview, event):
		from gtk.keysyms import Left, Right
		if event.keyval in (Left, Right): self.__index_async()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
