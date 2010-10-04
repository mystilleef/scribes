from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "deactivate", self.__deactivate_cb)
		self.connect(manager, "edit-points", self.__points_cb)
		self.connect(manager, "inserted-text", self.__inserted_cb)
		self.__sigid1 = self.connect(manager, "backspace", self.__backspace_cb)
		self.__sigid2 = self.connect(manager, "delete", self.__delete_cb)
		self.__block()
		editor.response()

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

	def __delete_with(self, method, mark):
		end = self.__buffer.get_iter_at_mark(mark)
		start = end.copy()
		result = start.backward_char() if method == "backspace" else start.forward_char()
		if result is False: return False
		self.__editor.response()
		self.__buffer.delete(start, end)
		self.__editor.response()
		return False

	def __remove_with(self, method):
		try:
			self.__editor.response()
			if not self.__marks: raise ValueError
			self.__buffer.begin_user_action()
			self.__editor.textview.window.freeze_updates()
			[self.__delete_with(method, mark) for mark in self.__marks]
			self.__editor.textview.window.thaw_updates()
			self.__buffer.end_user_action()
		except ValueError:
			self.__manager.emit("no-edit-point-error")
		finally:
			self.__editor.response()
		return False

	def __block(self):
		if self.__blocked: return False
		self.__manager.handler_block(self.__sigid1)
		self.__manager.handler_block(self.__sigid2)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__manager.handler_unblock(self.__sigid1)
		self.__manager.handler_unblock(self.__sigid2)
		self.__blocked = False
		return False

	def __handle(self, method):
		if self.__inserted_text is False: self.__manager.emit("inserted-text", True)
		self.__remove_with(method)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		self.__unblock()
		return False

	def __deactivate_cb(self, *args):
		self.__block()
		return False

	def __backspace_cb(self, *args):
		self.__handle("backspace")
		return True

	def __delete_cb(self, *args):
		self.__handle("delete")
		return False

	def __points_cb(self, manager, marks):
		self.__marks = marks
		return False

	def __inserted_cb(self, manager, inserted):
		self.__inserted_text = inserted
		return False
