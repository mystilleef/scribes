from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "show-full-view", self.__show_cb)
		self.connect(editor, "hide-full-view", self.__hide_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "show", self.__show_cb)
		self.connect(manager, "visible", self.__visible_cb)
		self.connect(editor, "window-focus-out", self.__focus_cb, True)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__container = editor.get_data("ToolContainer")
		self.__view = editor.textview
		self.__visible = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __pointer_on_toolbar(self):
		y = self.__editor.textview.window.get_pointer()[1]
		height = self.__editor.toolbar.size_request()[1]
		if y > 0 and y <= height: return True
		return False

	def __show(self, update=False):
		if self.__visible is True: return False
		self.__visible = True
		# Toolbar slide animation from up to down
		self.__manager.emit("slide", "down")
		return False

	def __hide(self):
		if self.__visible is False: return False
		self.__manager.emit("slide", "up")
		return False

	def __hide_cb(self, *args):
		if self.__pointer_on_toolbar(): return False
		self.__hide()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show, priority=9999)
		return False

	def __focus_cb(self, *args):
		self.__hide()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		return False
