from SCRIBES.SignalConnectionManager import SignalManager

class Container(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "show", self.__show_cb)
		self.__id = self.connect(self.__view, "expose-event", self.__expose_cb, True)
		self.__block()
		editor.register_object(self)
		self.__update_size()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__container = editor.get_data("ToolContainer")
		self.__view = editor.textview
		self.__blocked = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __show(self, update=False):
		self.__unblock()
		if update: self.__update_size()
		self.__editor.response()
		self.__container.hide()
		self.__container.show_all()
		self.__editor.response()
		return False

	def __hide(self):
		self.__block()
		self.__editor.response()
		self.__container.hide()
		self.__editor.response()
		return False

	def __update_size(self):
		from gtk import TEXT_WINDOW_WIDGET
		window = self.__view.get_window(TEXT_WINDOW_WIDGET)
		width = window.get_geometry()[2] + 2
		height = self.__editor.toolbar.size_request()[1]
		self.__editor.toolbar.set_size_request(width, height)
		return False

	def __block(self):
		if self.__blocked: return
		self.__view.handler_block(self.__id)
		self.__blocked = True
		return

	def __unblock(self):
		if not self.__blocked: return
		self.__view.handler_unblock(self.__id)
		self.__blocked = False
		return

	def __hide_cb(self, *args):
#		from gobject import idle_add
#		idle_add(self.__hide)
		self.__hide()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show, priority=9999)
		return False

	def __expose_cb(self, *args):
		self.__show(True)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
