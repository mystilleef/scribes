from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
#		self.connect(manager, "bar", self.__bar_cb)
#		self.connect(manager, "view-size", self.__view_size_cb)
#		self.connect(manager, "bar-size", self.__bar_size_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		self.__bwidth = 0
		self.__bheight = 0
		self.__vwidth = 0
		self.__vheight = 0
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __get_cordinates(self):
		if not self.__bar: return 0, 0
		vwidth, vheight = self.__vwidth, self.__vheight
		width, height = self.__bwidth, self.__bheight
		return vwidth - width, vheight - height + 2

	def __move(self):
		x, y = self.__get_cordinates()
		self.__view.move_child(self.__bar, x, y)
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		self.__move()
		return False

	def __bar_size_cb(self, manager, size):
		self.__bwidth, self.__bheight = size
		self.__move()
		return False

	def __view_size_cb(self, manager, size):
		self.__vwidth, self.__vheight = size
		self.__move()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
