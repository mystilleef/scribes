from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "up-key-press", self.__up_cb)
		self.connect(manager, "shift-up-key-press", self.__shift_up_cb)
		self.connect(manager, "down-key-press", self.__down_cb)
		self.connect(manager, "shift-down-key-press", self.__shift_down_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__view = manager.gui.get_object("TreeView")
		self.__model = self.__view.get_model()
		self.__selection = self.__view.get_selection()
		self.__column = self.__view.get_column(0)
		return

	def __up(self, multiple_selection=False):
		try:
			paths = self.__get_selected_paths()
			if not paths: raise ValueError
			row = paths[0][0]
			if not row: raise ValueError
			self.__select(row-1, multiple_selection)
		except ValueError:
			self.__manager.emit("focus-entry")
		return False

	def __down(self, multiple_selection=False):
		try:
			paths = self.__get_selected_paths()
			if not paths: raise ValueError
			row = paths[-1][0] + 1
			if row == len(self.__model): raise TypeError
			self.__select(row, multiple_selection)
		except ValueError:
			self.__manager.emit("focus-entry")
		except TypeError:
			if multiple_selection is False: self.__select_first_row()
		return False

	def __get_selected_paths(self):
		return self.__selection.get_selected_rows()[1]

	def __select_first_row(self):
		if not len(self.__model): return False
		path = self.__model[0].path
		self.__select(path)
		return False

	def __select(self, path, multiple_rows=False):
		self.__selection.select_path(path)
		if multiple_rows is False: self.__view.set_cursor(path, self.__column)
		self.__view.scroll_to_cell(path, self.__column)
		self.__view.grab_focus()
		return False

	def __up_cb(self, *args):
		self.__up()
		return False

	def __shift_up_cb(self, *args):
		self.__up(True)
		return False

	def __down_cb(self, *args):
		self.__down()
		return False

	def __shift_down_cb(self, *args):
		self.__down(True)
		return False
