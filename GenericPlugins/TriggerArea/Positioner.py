from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__widget.hide()
		from gtk import TEXT_WINDOW_WIDGET
		self.__view.add_child_in_window(self.__widget, TEXT_WINDOW_WIDGET, 0, -120)
		self.connect(editor.window, "configure-event", self.__event_cb)
		self.connect(editor, "scrollbar-visibility-update", self.__event_cb)
		self.connect(editor, "toolbar-is-visible", self.__show_cb, True)
		self.connect(editor, "show-full-view", self.__hide_cb)
		self.__position()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__widget = manager.get_data("TriggerWidget")
		self.__ignore_expose = False
		return

	def __get_cordinates(self, position):
		size = self.__widget.size
		from gtk import TEXT_WINDOW_WIDGET
		vwidth = self.__view.get_window(TEXT_WINDOW_WIDGET).get_geometry()[2]
		vheight = self.__view.get_window(TEXT_WINDOW_WIDGET).get_geometry()[3]
		cordinate = {
			"top-right": (vwidth - size, 0),
			"top-left": (0, 0),
			"bottom-right": (vwidth - size, vheight - size),
			"bottom-left": (0, vheight - size),
		}
		return cordinate[position]

	def __position(self):
		self.__widget.hide()
		position = self.__widget.position
		x, y = self.__get_cordinates(position)
		self.__view.move_child(self.__widget, x, y)
		self.__widget.show_all()
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
		self.__widget.hide()
		self.__view.move_child(self.__widget, 0, -120)
		return False

	def __event_cb(self, *args):
		if self.__ignore_expose: return False
		from gobject import idle_add
		idle_add(self.__position)
		return False
