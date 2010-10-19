from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "select-offsets", self.__select_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.__sigid1 = self.connect(editor, "cursor-moved", self.__moved_cb, True)
		self.__sigid2 = self.connect(editor.textview, "key-press-event", self.__event_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__blocked = False
		from collections import deque
		self.__offsets = deque([])
		self.__cursor_offset = 0
		self.__can_undo = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __reset(self):
		self.__block()
		self.__offsets.clear()
		self.__can_undo = False
		return False

	def __block(self):
		if self.__blocked: return False
		self.__editor.handler_block(self.__sigid1)
		self.__editor.textview.handler_block(self.__sigid2)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__editor.handler_unblock(self.__sigid1)
		self.__editor.textview.handler_unblock(self.__sigid2)
		self.__blocked = False
		return False

	def __previous_selection(self):
		try:
			if not self.__offsets: raise ValueError
			self.__offsets.pop()
			if not self.__offsets: raise ValueError
			offsets = self.__offsets[-1]
			get_iter = self.__editor.textbuffer.get_iter_at_offset
			start, end = get_iter(offsets[0]), get_iter(offsets[1])
			self.__editor.textbuffer.select_range(start, end)
		except ValueError:
			self.__reset()
			iterator = self.__editor.textbuffer.get_iter_at_offset(self.__cursor_offset)
			self.__editor.textbuffer.place_cursor(iterator)
		finally:
			self.__manager.emit("undo-selection")
		return False

	def __monitor_selection(self):
		try:
			if self.__editor.has_selection is False: raise ValueError
			start, end = self.__editor.selection_bounds
			selection = start.get_offset(), end.get_offset()
			if not (selection in self.__offsets): raise ValueError
		except ValueError:
			self.__reset()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __moved_cb(self, *args):
		self.__monitor_selection()
		return False

	def __select_cb(self, manager, offsets):
		self.__unblock()
		self.__offsets.append(offsets)
		self.__can_undo = True
		return False

	def __event_cb(self, view, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__previous_selection()
		return True

	def __activate_cb(self, *args):
		if self.__can_undo: return False
		self.__cursor_offset = self.__editor.cursor.get_offset()
		return False
