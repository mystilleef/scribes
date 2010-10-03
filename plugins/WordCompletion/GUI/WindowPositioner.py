from SCRIBES.SignalConnectionManager import SignalManager
ADJUSTMENT = 10

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "treeview-size", self.__size_cb)
		self.connect(manager, "show-window", self.__show_cb)
		self.connect(manager, "no-match-found", self.__hide_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.gui.get_widget("Window")
		self.__scroll = manager.gui.get_widget("ScrolledWindow")
		self.__is_visible = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __set_scroll_policy(self, data):
		width, height = data
		from gtk import POLICY_AUTOMATIC, POLICY_NEVER
		policy = POLICY_AUTOMATIC if height > 200 else POLICY_NEVER
		self.__scroll.set_policy(POLICY_NEVER, policy)
		return False

	def __get_size(self, data):
		width, height = data
		height = (200 + ADJUSTMENT) if height > 200 else (height + ADJUSTMENT)
		width = 200 if width < 200 else (width + ADJUSTMENT+10)
		return width, height

	def __get_x(self, width, cursor_data, textview_data):
		if self.__is_visible: return self.__window.get_position()[0]
		cursor_x, cursor_y, cursor_width, cursor_height = cursor_data
		textview_x, textview_y, textview_width, textview_height = textview_data
		# Determine default x coordinate of completion window.
		position_x = textview_x + cursor_x
		if (position_x + width) <= (textview_x + textview_width): return position_x
		# If the completion window extends past the text editor's buffer,
		# reposition the completion window inside the text editor's buffer area.
		return (textview_x + textview_width) - width

	def __get_y(self, height, cursor_data, textview_data):
		cursor_x, cursor_y, cursor_width, cursor_height = cursor_data
		textview_x, textview_y, textview_width, textview_height = textview_data
		# Determine default y coordinate of completion window.
		position_y = textview_y + cursor_y + cursor_height
		# If the completion window extends past the text editor's buffer,
		# reposition the completion window inside the text editor's buffer area.
		if (position_y + height) <= (textview_y + textview_height): return position_y
		return (textview_y + cursor_y) - height

	def __get_cursor_data(self):
		textview = self.__editor.textview
		rectangle = textview.get_iter_location(self.__editor.cursor)
		from gtk import TEXT_WINDOW_TEXT
		position = textview.buffer_to_window_coords(TEXT_WINDOW_TEXT, rectangle.x,
												rectangle.y)
		return position[0], position[1], rectangle.width, rectangle.height

	def __get_textview_data(self):
		from gtk import TEXT_WINDOW_TEXT
		window = self.__editor.textview.get_window(TEXT_WINDOW_TEXT)
		x, y = window.get_origin()
		rectangle = self.__editor.textview.get_visible_rect()
		return x, y, rectangle.width, rectangle.height

	def __get_cords(self, width, height):
		cursor_data = self.__get_cursor_data()
		textview_data = self.__get_textview_data()
		position_x = self.__get_x(width, cursor_data, textview_data)
		position_y = self.__get_y(height, cursor_data, textview_data)
		return position_x, position_y

	def __position_window(self, data):
		width, height = self.__get_size(data)
		xcord, ycord = self.__get_cords(width, height)
		self.__set_scroll_policy((width, height))
		self.__window.set_size_request(width, height)
		self.__window.resize(width, height)
		self.__window.move(xcord, ycord)
		self.__manager.emit("show-window")
		return False

	def __precompile_methods(self):
		methods = (self.__size_cb, self.__position_window,
			self.__get_size, self.__get_cords, self.__get_y,
			self.__get_x, self.__get_textview_data,
			self.__get_cursor_data,)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __size_cb(self, manager, data):
		self.__position_window(data)
		return False

	def __show_cb(self, *args):
		self.__is_visible = True
		return False

	def __hide_cb(self, *args):
		self.__is_visible = False
		return False
