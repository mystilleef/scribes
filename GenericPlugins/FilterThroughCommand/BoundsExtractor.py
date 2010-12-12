from SCRIBES.SignalConnectionManager import SignalManager

class Extractor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "bounds", self.__bounds_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "win", self.__win_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bounds = None
		return

	def __get_selected_bounds(self):
		start, end = self.__editor.selection_bounds
		start = self.__editor.backward_to_line_begin(start.copy())
		end = self.__editor.forward_to_line_end(end.copy())
		end.forward_char()
		return start, end

	def __extract(self):
		has_selection = self.__editor.has_selection
		bounds = self.__get_selected_bounds() if has_selection else self.__editor.textbuffer.get_bounds()
		self.__manager.emit("bounds", self.__mark(bounds))
		return

	def __mark(self, bounds):
		ml = self.__editor.create_left_mark
		mr = self.__editor.create_right_mark
		return ml(bounds[0]), mr(bounds[1])

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __activate_cb(self, *args):
		self.__extract()
		return False

	def __bounds_cb(self, manager, bounds):
		self.__bounds = bounds
		return False

	def __hide_cb(self, *args):
		[self.__editor.delete_mark(mark) for mark in self.__bounds]
		return False

	def __win_cb(self, *args):
		self.__manager.emit("bounds", self.__bounds)
		return False
