from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "bar", self.__bar_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bar = None
		self.__height = 0
		self.__width = 0
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self):
		width, height = self.__bar.size_request() # requisition.width, requisition.height
		if width == self.__width and height == self.__height: return False
		self.__width, self.__height = width, height
		self.__manager.emit("bar-size", (width, height))
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		self.connect(bar, "size-allocate", self.__size_cb)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __size_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__update, priority=PRIORITY_LOW)
		return False

	def __visible_cb(self, manager, visible):
		if visible: return False
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__update, priority=PRIORITY_LOW)
		return False
