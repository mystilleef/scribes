from SCRIBES.SignalConnectionManager import SignalManager

HIDE_TIMER = 7000

class Timer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__id = self.connect(editor.textview, "motion-notify-event", self.__motion_cb)
		self.connect(manager, "visible", self.__visible_cb)
		self.connect(editor, "quit", self.__quit_cb)
		self.__block()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__visible = False
		self.__blocked = None
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __hide(self):
		try:
			hide = lambda: self.__manager.emit("hide")
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(HIDE_TIMER, hide)
		return False

	def __block(self):
		if self.__blocked is True: return False
		self.__blocked = True
		self.__view.handler_block(self.__id)
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__blocked = False
		self.__view.handler_unblock(self.__id)
		return False

	def __motion_cb(self, *args):
		if self.__visible is False: return False
		self.__hide()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		self.__unblock() if visible else self.__block()
		if visible: self.__hide()
		return False
