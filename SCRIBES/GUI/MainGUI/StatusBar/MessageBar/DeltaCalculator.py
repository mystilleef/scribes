from SCRIBES.SignalConnectionManager import SignalManager

REFRESH_TIME = 5 # units in milliseconds
ANIMATION_TIME = 250 # units in milliseconds

class Calculator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "bar-size", self.__size_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from SCRIBES.GObjectTimerManager import Manager
		self.__timer_manager = Manager()
		return

	def __destroy(self):
		self.__timer_manager.destroy()
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self, size):
		width, height = size
		hdelta = float(width) / float(ANIMATION_TIME / REFRESH_TIME)
		vdelta = float(height) / float(ANIMATION_TIME / REFRESH_TIME)
		self.__manager.emit("deltas", (int(round(hdelta)), int(round(vdelta))))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __size_cb(self, manager, size):
		self.__timer_manager.remove_all()
		from gobject import idle_add
		self.__timer1 = idle_add(self.__update, size)
		self.__timer_manager.add(self.__timer1)
		return False
