from SCRIBES.SignalConnectionManager import SignalManager

class Sensor(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__id1 = self.connect(editor.textview, "motion-notify-event", self.__motion_cb, True)
		self.connect(editor, "message-bar-is-visible", self.__visible_cb)
		self.connect(editor, "quit", self.__quit_cb)
		editor.register_object(self)
		editor.response()
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__visible = False
		self.__blocked = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __show(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = idle_add(self.__emit)
		return False

	def __emit(self):
		self.__reset()
		self.__manager.emit("show-message")
		return False

	def __reset(self):
		try:
			reset = lambda: self.__manager.emit("reset")
			from gobject import timeout_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = timeout_add(750, reset)
		return False

	def __block(self):
		if self.__blocked is True: return False
		self.__blocked = True
		self.__view.handler_block(self.__id1)
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__blocked = False
		self.__view.handler_unblock(self.__id1)
		return False

	def __motion_cb(self, *args):
		self.__show()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		self.__unblock() if visible else self.__block()
		return False
