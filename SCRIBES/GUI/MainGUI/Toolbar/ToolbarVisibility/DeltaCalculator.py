from SCRIBES.SignalConnectionManager import SignalManager

REFRESH_TIME = 5 # units in milliseconds
ANIMATION_TIME = 250 # units in milliseconds

class Calculator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "size", self.__size_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 
	
	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self 
		return False

	def __update(self, size):
		width, height = size
		hdelta = float(width) / float(ANIMATION_TIME / REFRESH_TIME)
		vdelta = float(height) / float(ANIMATION_TIME / REFRESH_TIME)
		self.__manager.emit("deltas", (round(hdelta), round(vdelta)))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
	
	def __size_cb(self, manager, size):
		self.__update(size)
		return False
