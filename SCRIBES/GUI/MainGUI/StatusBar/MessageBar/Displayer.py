from SCRIBES.SignalConnectionManager import SignalManager

class Displayer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "bar", self.__bar_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "show", self.__show_cb)
		self.__id = self.connect(self.__view, "expose-event", self.__reposition_cb, True)
		self.__block()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		self.__blocked = False
		self.__count = 0
		self.__visible = False
		self.__x, self.__y = self.__get_cordinates()
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __hide(self):
		self.__visible = False
		self.__block()
		self.__editor.response()
		self.__bar.hide()
		self.__editor.response()
		return False

	def __show(self, conditional_show=False):
		cordinates_changed = self.__cordinates_changed()
		if conditional_show and not cordinates_changed: return False
		self.__unblock()
		self.__editor.response()
		# only show if cordinates have changed
		if not cordinates_changed and self.__visible: return False
		self.__move()
		self.__bar.show_all()
		self.__editor.response()
		self.__visible = True
		return False

	def __cordinates_changed(self):
		x, y = self.__get_cordinates()
		if x == self.__x and y == self.__y: return False
		return True

	def __update_cordinates(self):
		self.__x, self.__y = self.__get_cordinates()
		return False

	def __get_cordinates(self):
		if not self.__bar: return 0, 0
		geometry = self.__view.window.get_geometry()
		vwidth, vheight = geometry[2], geometry[3]
		width, height = self.__bar.size_request()
		return vwidth - width + 3, vheight - height + 4

	def __move(self):
		self.__bar.hide()
		self.__update_cordinates()
		self.__view.move_child(self.__bar, self.__x, self.__y)
		return False

	def __reposition(self):
		if not self.__visible: return False
		self.__show(True)
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

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		self.__move()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __reposition_cb(self, *args):
		self.__reposition()
		return False
