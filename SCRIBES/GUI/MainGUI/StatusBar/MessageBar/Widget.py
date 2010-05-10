from SCRIBES.SignalConnectionManager import SignalManager

class Widget(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__setup()
		self.__emit()
		self.__update_public_api()
		self.connect(editor, "quit", self.__quit_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = self.__get_label()
		self.__button = self.__get_button()
		self.__bar = self.__get_bar()
		from gtk import HBox, Image
		self.__box = HBox(False, 5)
		self.__image = Image()
		self.__view = editor.textview
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __setup(self):
		from gtk import TEXT_WINDOW_WIDGET
		self.__view.add_child_in_window(self.__bar, TEXT_WINDOW_WIDGET, 0, -100)
		self.__bar.add(self.__button)
		self.__button.add(self.__box)
		self.__box.pack_start(self.__image, False, False)
		self.__box.pack_start(self.__label, False, False)
		self.__bar.realize()
		return False

	def __emit(self):
		self.__manager.emit("bar", self.__bar)
		return False

	def __update_public_api(self):
		self.__editor.set_data("MessageBar", self.__manager)
		self.__editor.set_data("StatusImage", self.__image)
		self.__editor.set_data("StatusFeedback", self.__label)
		return False

	def __get_bar(self):
		from gtk import EventBox
		bar = EventBox()
		return bar

	def __get_label(self):
		from gtk import Label
		label = Label()
		label.set_property("single-line-mode", True)
		label.set_property("use-markup", True)
		return label

	def __get_button(self):
		from gtk import Button
		button = Button()
		button.set_property("focus-on-click", False)
		button.set_property("can-default", False)
		button.set_property("can-focus", False)
		button.set_property("has-default", False)
		button.set_property("is-focus", False)
		button.set_property("receives-default", False)
		button.set_property("receives-default", False)
		return button

	def __quit_cb(self, *args):
		self.__destroy()
		return False
