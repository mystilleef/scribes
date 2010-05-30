from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		from gtk import TEXT_WINDOW_WIDGET
		self.__view.add_child_in_window(self.__tbox, TEXT_WINDOW_WIDGET, -100, -100)
		self.connect(editor.window, "expose-event", self.__expose_cb)
		self.__position()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__twidth = 24
		self.__tbox = manager.get_data("TriggerWidget")
		return

	def __position(self):
		self.__tbox.hide()
		from gtk import TEXT_WINDOW_WIDGET
		vwidth = self.__view.get_window(TEXT_WINDOW_WIDGET).get_geometry()[2]
		self.__view.move_child(self.__tbox, vwidth - self.__twidth, 0)
		self.__tbox.show_all()
		return False

	def __expose_cb(self, *args):
		self.__position()
		return False
