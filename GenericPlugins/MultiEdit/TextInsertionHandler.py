from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "deactivate", self.__deactivate_cb)
		self.connect(manager, "edit-points", self.__points_cb)
		self.connect(manager, "clear", self.__clear_cb)
		self.__sigid1 = self.connect(editor.textbuffer, "insert-text", self.__insert_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__blocked = False
		self.__buffer = editor.textbuffer
		self.__marks = []
		self.__inserted_text = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __insert_text_at(self, mark, text):
		iterator = self.__buffer.get_iter_at_mark(mark)
		self.__editor.refresh(False)
		self.__buffer.insert(iterator, text)
		self.__editor.refresh(False)
		return False

	def __insert(self, text):
		try:
			if not self.__marks: raise ValueError
			self.__editor.textview.window.freeze_updates()
			self.__block()
			self.__buffer.begin_user_action()
			[self.__insert_text_at(mark, text) for mark in self.__marks]
			self.__buffer.end_user_action()
			self.__unblock()
			self.__editor.textview.window.thaw_updates()
		except ValueError:
			self.__manager.emit("no-edit-point-error")
		return False

	def __block(self):
		if self.__blocked: return False
		self.__buffer.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__buffer.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __emit(self, inserted):
		self.__manager.emit("inserted-text", inserted)
		self.__inserted_text = inserted
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		self.__unblock()
		return False

	def __deactivate_cb(self, *args):
		self.__block()
		self.__emit(False)
		return False

	def __insert_cb(self, textbuffer, iterator, text, length):
		if self.__inserted_text is False: self.__emit(True)
		self.__buffer.emit_stop_by_name("insert-text")
		self.__insert(text)
		return True

	def __points_cb(self, manager, marks):
		self.__marks = marks
		return False

	def __clear_cb(self, *args):
		self.__emit(False)
		return False
