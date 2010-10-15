from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__set_properties()
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.main_gui.get_object("TreeView")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __set_properties(self):
		self.__treeview.append_column(self.__create_column())
		self.__treeview.set_model(self.__create_model())
		from gtk import SELECTION_MULTIPLE
		self.__treeview.get_selection().set_mode(SELECTION_MULTIPLE)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_OBJECT
		model = ListStore(str, TYPE_OBJECT, bool)
		return model

	def __create_column(self):
		from gtk import TreeViewColumn, CellRendererText, TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		renderer = CellRendererText()
		column.pack_start(renderer, False)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(False)
		column.set_attributes(renderer, text=0)
		return column

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
