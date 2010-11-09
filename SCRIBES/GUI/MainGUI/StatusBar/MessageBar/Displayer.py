from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "bar", self.__bar_cb)
		self.connect(manager, "_hide", self.__hide_cb)
		self.connect(manager, "_show", self.__show_cb)
		self.connect(manager, "bar-size", self.__bsize_cb)
		self.connect(manager, "view-size", self.__vsize_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		self.__visible = False
		self.__bwidth, self.__bheight = 0, 0
		self.__vwidth, self.__vheight = 0, 0
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __hide(self):
		if self.__pointer_on_messagebar(): return False
		self.__manager.emit("slide", "down")
		return False

	def __show(self):
		self.__manager.emit("slide", "up")
		return False

	def __pointer_on_messagebar(self):
		x, y, mask = self.__editor.textview.window.get_pointer()
		hvalue = y >= (self.__vheight - self.__bheight) and y <= self.__vheight
		wvalue = x >= (self.__vwidth - self.__bwidth) and x <= self.__vwidth
		if hvalue and wvalue: return True
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide)
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __vsize_cb(self, manager, size):
		self.__vwidth, self.__vheight = size
		return False

	def __bsize_cb(self, manager, size):
		self.__bwidth, self.__bheight = size
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
