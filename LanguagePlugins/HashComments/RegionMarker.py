from SCRIBES.SignalConnectionManager import SignalManager

class Marker(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__rmark = editor.create_right_mark()
		self.__lmark = editor.create_left_mark()
		return

	def __mark(self):
		editor = self.__editor
		start, end = self.__get_selection_bounds() if editor.has_selection else editor.line_bounds
		editor.textbuffer.move_mark(self.__lmark, start)
		editor.textbuffer.move_mark(self.__rmark, end)
		from gobject import idle_add
		idle_add(self.__manager.emit, "region-marks", (self.__lmark, self.__rmark))
		return False

	def __get_selection_bounds(self):
		start, end = self.__editor.selection_bounds
		start = self.__editor.backward_to_line_begin(start)
		end = self.__editor.forward_to_line_end(end)
		return start, end

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__mark)
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
