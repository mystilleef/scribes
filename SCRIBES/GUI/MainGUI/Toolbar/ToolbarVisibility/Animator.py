from SCRIBES.SignalConnectionManager import SignalManager

REFRESH_TIME = 5 # units in milliseconds

class Animator(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "slide", self.__slide_cb)
		self.connect(manager, "deltas", self.__deltas_cb)
		self.connect(manager, "size", self.__size_cb)
		from gobject import idle_add
		idle_add(self.__compile, priority=9999)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__container = editor.get_data("ToolContainer")
		self.__start_point = 0
		self.__end_point = 0
		self.__hdelta = 0
		self.__vdelta = 0
		self.__height =0
		self.__width = 0
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __slide(self, direction="left"):
		try:
			self.__manager.emit("animation", "begin")
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__update_animation_start_point(direction)
			self.__update_animation_end_point(direction)
			self.__timer = timeout_add(REFRESH_TIME, self.__move, direction, priority=9999)
		return False

	def __move_on_idle(self, direction):
		try:
			x = int(self.__get_x(direction))
			y = int(self.__get_y(direction))
			self.__editor.response()
			self.__editor.textview.move_child(self.__container, x, y)
			if not self.__container.get_property("visible"): self.__container.show_all()
			self.__editor.response()
		except AttributeError:
			pass
		return False

	def __move(self, direction):
		try:
			animate = True
			self.__can_end(direction)
			try:
				from gobject import idle_add, source_remove
				source_remove(self.__timer1)
			except AttributeError:
				pass
			finally:
				self.__timer1 = idle_add(self.__move_on_idle, direction, priority=9999)
		except ValueError:
			animate = False
			self.__manager.emit("animation", "end")
		return animate

	def __can_end(self, direction):
#		if direction == "left" and self.__start_point <= -2: raise ValueError
		if direction == "up" and self.__start_point <= -self.__height - 4: raise ValueError
		if direction == "down" and self.__start_point >= -2: raise ValueError
		return False

	def __get_x(self, direction):
		if direction in ("up", "down"): return -2
		if direction == "left": self.__start_point -= self.__hdelta
		if direction == "right": self.__start_point += self.__hdelta
		if self.__start_point < -2: return -2
		return self.__start_point

	def __get_y(self, direction):
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

	def __compile(self):
		self.__editor.optimize((self.__move, self.__move_on_idle))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __slide_cb(self, manager, direction):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__ttimer)
		except AttributeError:
			pass
		finally:
			self.__ttimer = idle_add(self.__slide, direction, priority=9999)
		return False

	def __deltas_cb(self, manager, deltas):
		self.__hdelta, self.__vdelta = deltas
		return False

	def __size_cb(self, manager, size):
		self.__width, self.__height = size
		return False
