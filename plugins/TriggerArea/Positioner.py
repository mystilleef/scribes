from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__tbox.hide()
		from gtk import TEXT_WINDOW_WIDGET
		self.__view.add_child_in_window(self.__tbox, TEXT_WINDOW_WIDGET, 0, 0)
		self.connect(editor.window, "expose-event", self.__expose_cb)
		self.__position()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__tbox = manager.get_data("TriggerWidget")
		return

	def __position(self):
		self.__editor.response()
		self.__tbox.hide()
		position = self.__tbox.position
		size = self.__tbox.size
		from gtk import TEXT_WINDOW_WIDGET
		vwidth = self.__view.get_window(TEXT_WINDOW_WIDGET).get_geometry()[2]
		vheight = self.__view.get_window(TEXT_WINDOW_WIDGET).get_geometry()[3]
		cordinate = {
			"top-right": (vwidth - size, 0),
			"top-left": (0, 0),
			"bottom-right": (vwidth - size, vheight - size),
			"bottom-left": (0, vheight - size),
		}
		x, y = cordinate[position]
		self.__view.move_child(self.__tbox, x, y)
		self.__tbox.show_all()
		self.__editor.response()
		return False

	def __expose_cb(self, *args):
		self.__position()
		return False
