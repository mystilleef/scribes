from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "updated-model", self.__updated_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		self.__selection = self.__view.get_selection()
		self.__column = self.__view.get_column(0)
		self.__model = self.__view.get_model()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

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
