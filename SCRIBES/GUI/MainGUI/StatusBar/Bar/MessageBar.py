VIEW_BOTTOM_BORDER_SIZE = 0

class MessageBar(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__setup_widgets()
		editor.set_data("MessageBar", self)
		editor.set_data("StatusImage", self.__image)
		editor.set_data("StatusFeedback", self.__label)
		self.__id = self.__view.connect("expose-event", self.__expose_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from gtk import EventBox, Image, Label, Button
		self.__bar = EventBox()
		self.__image = Image()
		self.__label = Label()
		self.__label.set_use_markup(True)
		self.__button = Button()
		self.__view = editor.textview
		self.__blocked = False
		self.__x, self.__y = self.__get_cordinates()
		return

	def __get_cordinates(self):
		rectangle = self.__view.get_visible_rect()
		width, height = self.__bar.size_request()
		return -3, rectangle.height - height + 4 + VIEW_BOTTOM_BORDER_SIZE

	def __update_cordinates(self):
		self.__x, self.__y = self.__get_cordinates()
		return False

	def __setup_widgets(self):
		from gtk import HBox, TEXT_WINDOW_WIDGET, TEXT_WINDOW_BOTTOM
		box = HBox(False, 5)
		box.pack_start(self.__image, False, False)
		box.pack_start(self.__label, False, False)
		self.__button.add(box)
		self.__bar.add(self.__button)
		self.__view.add_child_in_window(self.__bar, TEXT_WINDOW_WIDGET, 0, 0)
#		self.__view.set_border_window_size(TEXT_WINDOW_BOTTOM, 7)
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

	def show(self, update=False):
		self.__unblock()
		if update: self.__update_cordinates()
		self.__view.move_child(self.__bar, self.__x, self.__y)
		self.__bar.show_all()
		return True 

	def hide(self):
		self.__block()
		self.__bar.hide()
		return False

	def __expose_cb(self, *args):
		self.show(True)
		return False
