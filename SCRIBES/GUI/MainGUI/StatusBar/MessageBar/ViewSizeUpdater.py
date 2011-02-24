from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor.window, "configure-event", self.__event_cb)
		self.connect(editor, "scrollbar-visibility-update", self.__event_cb, True)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self):
		geometry = self.__view.window.get_geometry()
		width, height = geometry[2], geometry[3]
		self.__manager.emit("view-size", (width, height))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __event_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False
