from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(self.__view, "size-allocate", self.__update_cb, True)
		self.connect(editor, "scrollbar-visibility-update", self.__update_cb, True)
		self.connect(editor.window, "configure-event", self.__update_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__width = 0
		self.__height = 0
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self):
		self.__editor.refresh(False)
		geometry = self.__view.window.get_geometry()
		width, height = geometry[2], geometry[3]
		if self.__width == width and self.__height == height: return False
		self.__width, self.__height = width, height
		self.__manager.emit("view-size", (width, height))
		return False

	def __update_on_idle(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__update, priority=PRIORITY_LOW)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(250, self.__update_on_idle, priority=PRIORITY_LOW)
		return False
