from SCRIBES.SignalConnectionManager import SignalManager

REFRESH_TIME = 5 # units in milliseconds

class Animator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "slide", self.__slide_cb)
		self.connect(manager, "deltas", self.__deltas_cb)
		self.connect(manager, "size", self.__size_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.view
		self.__container = editor.get_data("ToolContainer")
		self.__start_point = 0
		self.__end_point = 0
		self.__hdelta = 0
		self.__vdelta = 0
		self.__height = 0
		self.__width = 0
		self.__busy = False
		self.__count = 0
		return


	def __slide(self, direction="left"):
		self.__manager.emit("animation", "begin")
		self.__update_animation_start_point(direction)
		self.__update_animation_end_point(direction)
		from gobject import timeout_add
		self.__timer1 = timeout_add(REFRESH_TIME, self.__move, direction)
		return False

	def __move(self, direction):
		try:
			if self.__count >= 50: raise ValueError
			self.__count += 1
			self.__editor.refresh(False)
			animate = True
			self.__can_end(direction)
			self.__reposition_in(direction)
		except ValueError:
			self.__remove_all_timers()
			self.__editor.refresh(False)
			if direction == "up": self.__container.hide()
			self.__editor.refresh(False)
			self.__manager.emit("animation", "end")
			animate = False
			self.__busy = False
			self.__count = 0
		return animate

	def __can_end(self, direction):
		self.__editor.refresh(False)
		if direction == "up" and self.__start_point <= -self.__height - 4: raise ValueError
		if direction == "down" and self.__start_point >= -2: raise ValueError
		return False

	def __reposition_in(self, direction):
		try:
			x = int(self.__get_x(direction))
			y = int(self.__get_y(direction))
			self.__editor.refresh(False)
			self.__view.move_child(self.__container, x, y)
			self.__editor.refresh(False)
			self.__container.show_all()
			self.__editor.refresh(False)
		except AttributeError:
			pass
		return False

	def __get_x(self, direction):
		self.__editor.refresh(False)
		if direction in ("up", "down"): return -2
		if direction == "left": self.__start_point -= self.__hdelta
		if direction == "right": self.__start_point += self.__hdelta
		if self.__start_point < -2: return -2
		return self.__start_point

	def __get_y(self, direction):
		self.__editor.refresh(False)
		if direction in ("left", "right"): return -2
		if direction == "up": self.__start_point -= self.__vdelta
		if direction == "down": self.__start_point += self.__vdelta
		if self.__start_point >= -2: return -2
		return self.__start_point

	def __update_animation_start_point(self, direction):
		dictionary = {
			"up": -2,
			"down": -self.__height,
			"left": self.__width,
			"right":0,
		}
		self.__start_point = dictionary[direction]
		return False

	def __update_animation_end_point(self, direction):
		dictionary = {
			"up": -self.__height - 4,
			"down": -2,
			"left": -2,
			"right": self.__width,
		}
		self.__end_point = dictionary[direction]
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

	def __compile(self):
		self.__editor.optimize((self.__move, self.__reposition_in))
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __slide_cb(self, manager, direction):
		if self.__busy: return False
		self.__busy = True
		self.__remove_all_timers()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__slide, direction, priority=PRIORITY_LOW)
		return False

	def __deltas_cb(self, manager, deltas):
		self.__hdelta, self.__vdelta = deltas
		return False

	def __size_cb(self, manager, size):
		self.__width, self.__height = size
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
