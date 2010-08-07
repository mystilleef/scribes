from SCRIBES.SignalConnectionManager import SignalManager

OFFSET = 4
REFRESH_TIME = 5 # units in milliseconds

class Animator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "slide", self.__slide_cb, True)
		self.connect(manager, "deltas", self.__deltas_cb)
		self.connect(manager, "bar-size", self.__bsize_cb)
		self.connect(manager, "view-size", self.__vsize_cb)
		self.connect(manager, "bar", self.__bar_cb)
		from gobject import idle_add
		idle_add(self.__compile, priority=9999)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		self.__start_point = 0
		self.__end_point = 0
		self.__hdelta = 0
		self.__vdelta = 0
		self.__bheight =0
		self.__bwidth = 0
		self.__vheight =0
		self.__vwidth = 0
		self.__busy = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __slide(self, direction):
		try:
			self.__manager.emit("animation", "begin")
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__update_animation_start_point(direction)
			self.__update_animation_end_point(direction)
			self.__timer = timeout_add(REFRESH_TIME, self.__move, direction)
		return False

	def __reposition_in(self, direction):
		try:
			x = int(self.__get_x(direction))
			y = int(self.__get_y(direction))
			self.__editor.response()
			self.__editor.textview.move_child(self.__bar, x, y)
			if not self.__bar.get_property("visible"): self.__bar.show_all()
			self.__editor.response()
		except AttributeError:
			pass
		return False

	def __move(self, direction):
		try:
			animate = True
			self.__can_end(direction)
			self.__reposition_in(direction)
		except ValueError:
			animate = False
			if direction == "down": self.__bar.hide()
			self.__manager.emit("animation", "end")
			self.__busy = False
		return animate

	def __can_end(self, direction):
		if direction == "down" and self.__start_point >= self.__end_point: raise ValueError
		if direction == "up" and self.__start_point <= self.__end_point: raise ValueError
		return False

	def __get_x(self, direction):
		if direction in ("up", "down"): return self.__vwidth - self.__bwidth + 4
		if direction == "left": self.__start_point -= self.__hdelta
		if direction == "right": self.__start_point += self.__hdelta
		x = self.__vwidth - self.__bwidth
		if self.__start_point <= x: return x + OFFSET
		return self.__start_point

	def __get_y(self, direction):
		if direction in ("left", "right"): return self.__vheight - self.__bheight + 4
		if direction == "up": self.__start_point -= self.__vdelta
		if direction == "down": self.__start_point += self.__vdelta
#		if self.__start_point > self.__vheight + 4: return self.__vheight + 4
#		if self.__start_point < self.__end_point: return self.__end_point
		return self.__start_point

	def __update_animation_start_point(self, direction):
		dictionary = {
			"up": self.__vheight,
			"down": self.__vheight - self.__bheight + 4,
			"left": self.__vwidth,
			"right":0,
		}
		self.__start_point = dictionary[direction]
		return False

	def __update_animation_end_point(self, direction):
		dictionary = {
			"up": self.__vheight - self.__bheight + 4,
			"down": self.__vheight + 4,
			"left": self.__vwidth - self.__bwidth + 4,
			"right": self.__bwidth,
		}
		self.__end_point = dictionary[direction]
		return False

	def __compile(self):
		self.__editor.optimize((self.__move, self.__reposition_in))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __slide_cb(self, manager, direction):
		if not self.__bar: return False
		if self.__busy: return False
		try:
			self.__busy = True
			from gobject import idle_add, source_remove
			source_remove(self.__timer2)
		except AttributeError:
			pass
		finally:
			self.__timer2 = idle_add(self.__slide, direction, priority=9999)
		return False

	def __deltas_cb(self, manager, deltas):
		self.__hdelta, self.__vdelta = deltas
		return False

	def __bsize_cb(self, manager, size):
		self.__bwidth, self.__bheight = size
		return False

	def __vsize_cb(self, manager, size):
		self.__vwidth, self.__vheight = size
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		self.__bar.show_all()
		return False
