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
			self.__timer = timeout_add(REFRESH_TIME, self.__move, direction)
		return False

	def __move(self, direction):
		try:
			animate = True
			self.__can_end(direction)
			x = int(self.__get_x(direction))
			y = int(self.__get_y(direction))
			self.__editor.textview.move_child(self.__container, x, y)
			self.__container.show_all()
		except ValueError:
			animate = False
			self.__manager.emit("animation", "end")
		return animate 

	def __can_end(self, direction):
		if direction == "left" and self.__start_point <= -2: raise ValueError
		if direction == "up" and self.__start_point <= -self.__height - 4: raise ValueError
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
		return self.__start_point

	def __update_animation_start_point(self, direction):
		dictionary = {
			"up": -2,
			"down": 0,
			"left": self.__width,
			"right":0,
		}
		self.__start_point = dictionary[direction]
		return False
	
	def __update_animation_end_point(self, direction):
		dictionary = {
			"up": -self.__height - 4,
			"down": -self.__height,
			"left": -2,
			"right": self.__width,
		}
		self.__end_point = dictionary[direction]
		return False

	def __end_animation(self):
		self.__container.hide()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
	
	def __slide_cb(self, manager, direction):
		self.__slide(direction)
		return False

	def __deltas_cb(self, manager, deltas):
		self.__hdelta, self.__vdelta = deltas
		return False
	
	def __size_cb(self, manager, size):
		self.__width, self.__height = size
		return False
