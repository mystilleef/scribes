from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(self.__view, "expose-event", self.__expose_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__height = 0
		self.__width = 0
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self): 
		geometry = self.__view.window.get_geometry()
		width, height = geometry[2], geometry[3]
		if width == self.__width and height == self.__height: return False
		self.__width, self.__height = width, height
		self.__manager.emit("view-size", (width, height))
		return False 

	def __quit_cb(self, *args):
		self.__destroy()
		return False 

	def __expose_cb(self, *args):
		self.__update()
		return False
