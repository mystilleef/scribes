from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "updated-model", self.__updated_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__view = manager.gui.get_object("TreeView")
		self.__selection = self.__view.get_selection()
		self.__column = self.__view.get_column(0)
		self.__model = self.__view.get_model()
		return

	def __select(self):
		try:
			if not len(self.__model): raise ValueError
			self.__selection.select_path(0)
			self.__view.set_cursor(0, self.__column)
			self.__view.scroll_to_cell(0, None, True, 0.5, 0.5)
		except ValueError:
			pass
		finally:
			self.__manager.emit("selected-row")
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __updated_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add
		self.__timer = idle_add(self.__select)
		return False
