from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor.window, "configure-event", self.__event_cb)
		self.connect(editor, "scrollbar-visibility-update", self.__event_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__width = 0
		self.__height = 0
		self.__count = 0
		self.__pount = 0
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self):
		width = self.__get_width()
		height = self.__get_height()
		if width == self.__width and height == self.__height: return False
		self.__width, self.__height = width, height
		self.__manager.emit("size", (width, height))
		return False

	def __get_width(self):
		from gtk import TEXT_WINDOW_WIDGET
		window = self.__editor.textview.get_window(TEXT_WINDOW_WIDGET)
		return window.get_geometry()[2]

	def __get_height(self):
		height = self.__editor.toolbar.size_request()[1]
		return height

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __event_cb(self, *args):
		self.__remove_timer(1)
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(self.__update, priority=PRIORITY_LOW)
		return False
