from SCRIBES.SignalConnectionManager import SignalManager

class Sensor(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor.textview, "motion-notify-event", self.__motion_cb)
		self.connect(editor, "quit", self.__quit_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __show(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = idle_add(self.__emit, priority=9999)
		return False

	def __show_bar(self):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = timeout_add(250, self.__emit, priority=9999)
		return False

	def __emit(self):
		self.__manager.emit("show-message")
		self.__reset()
		return False

	def __reset(self):
		try:
			reset = lambda: self.__manager.emit("reset")
			from gobject import timeout_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = timeout_add(5000, reset, priority=9999)
		return False

	def __motion_cb(self, *args):
		self.__show()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
