from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "updated-model", self.__updated_cb)
		self.connect(manager, "theme-from-database", self.__theme_cb)
		self.connect(manager, "last-selected-path", self.__path_cb)
		self.connect(manager, "activate", self.__activate_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.main_gui.get_object("TreeView")
		self.__selection = self.__treeview.get_selection()
		self.__column = self.__treeview.get_column(0)
		self.__model = self.__treeview.get_model()
		self.__theme = ""
		self.__path = (0,)
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __get_scheme_row(self, theme):
		if not theme: return None
		row = None
		for _row in self.__model:
			self.__editor.refresh()
			if _row[1].get_id() != theme: continue
			row = _row
			break
		return row

	def __sel(self, iterator, path):
		self.__selection.select_iter(iterator)
		self.__treeview.grab_focus()
		self.__treeview.set_cursor(path, self.__column)
		self.__treeview.scroll_to_cell(path, None, True, 0.5, 0.5)
		self.__manager.emit("selected-row")
		return False

	def __is_selected(self, row):
		return self.__selection.iter_is_selected(row.iter)

	def __select_row_from_theme(self):
		row = self.__get_scheme_row(self.__theme)
		if not row: raise ValueError
		if self.__is_selected(row): return False
		self.__manager.emit("ignore-row-activation", True)
		self.__sel(row.iter, row.path)
		self.__manager.emit("ignore-row-activation", False)
		return False

	def __select_row_from_path(self):
		try:
			path = self.__path
			iterator = self.__model.get_iter(path)
			self.__sel(iterator, path)
		except ValueError:
			row = self.__model[-1]
			self.__sel(row.iter, row.path)
		return False

	def __select(self):
		if not len(self.__model): return False
		try:
			self.__select_row_from_theme()
		except ValueError:
			self.__select_row_from_path()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__select)
		return False

	def __theme_cb(self, manager, theme):
		self.__theme = theme
		return False

	def __path_cb(self, manager, path):
		self.__path = path
		return False

	def __activate_cb(self, *args):
		self.__select()
		return False
