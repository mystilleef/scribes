from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__tbox.hide()
		from gtk import TEXT_WINDOW_WIDGET
		self.__view.add_child_in_window(self.__tbox, TEXT_WINDOW_WIDGET, 0, 0)
		self.connect(editor.window, "expose-event", self.__expose_cb)
		self.connect(editor, "toolbar-is-visible", self.__show_cb, True)
		self.connect(editor, "show-full-view", self.__hide_cb)
		self.__position()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__tbox = manager.get_data("TriggerWidget")
		self.__ignore_expose = False
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

	def __show(self):
		self.__ignore_expose = False
		self.__position()
		return False

	def __show_cb(self, editor, visible):
		if visible: return False
		from gobject import timeout_add
		timeout_add(500, self.__show, priority=9999)
		return False

	def __hide_cb(self, *args):
		self.__ignore_expose = True
		self.__editor.response()
		self.__tbox.hide()
		self.__view.move_child(self.__tbox, 0, -120)
		self.__editor.response()
		return False

	def __expose_cb(self, *args):
		if self.__ignore_expose: return False
		self.__position()
		return False
