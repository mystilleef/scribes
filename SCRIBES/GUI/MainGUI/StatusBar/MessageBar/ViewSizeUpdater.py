from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "close", self.__quit_cb)
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
		from SCRIBES.GObjectTimerManager import Manager
		self.__timer_manager = Manager()
		return

	def __destroy(self):
		self.disconnect()
		self.__timer_manager.destroy()
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
		from gobject import idle_add
		self.__timer2 = idle_add(self.__update)
		self.__timer_manager.add(self.__timer2)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		self.__timer_manager.remove_all()
		from gobject import timeout_add
		self.__timer1 = timeout_add(25, self.__update_on_idle)
		self.__timer_manager.add(self.__timer1)
		return False
