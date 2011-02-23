from SCRIBES.SignalConnectionManager import SignalManager

class Resizer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "size", self.__size_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update_size(self):
		from gtk import TEXT_WINDOW_WIDGET
		window = self.__editor.textview.get_window(TEXT_WINDOW_WIDGET)
		width = window.get_geometry()[2] + 2
		height = self.__editor.toolbar.size_request()[1]
		self.__editor.toolbar.set_size_request(width, height)
		return False

	def __size_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update_size)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
