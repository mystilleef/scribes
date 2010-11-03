from SCRIBES.SignalConnectionManager import SignalManager

class Initializer(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.__set_properties()

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__treeview = manager.gui.get_object("TreeView")
		return

	def __set_properties(self):
		self.__treeview.append_column(self.__create_column())
		self.__treeview.set_model(self.__create_model())
		from gtk import SELECTION_MULTIPLE
		self.__treeview.get_selection().set_mode(SELECTION_MULTIPLE)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_OBJECT
		model = ListStore(TYPE_OBJECT, str, str)
		return model

	def __create_column(self):
		from gtk import TreeViewColumn, CellRendererText, TREE_VIEW_COLUMN_FIXED
		from gtk import CellRendererPixbuf
		column = TreeViewColumn()
		txt_renderer = CellRendererText()
		txt_renderer.props.ypad = 10
		txt_renderer.props.xpad = 10
		pb_renderer = CellRendererPixbuf()
		pb_renderer.props.ypad = 10
		pb_renderer.props.xpad = 10
		column.pack_start(pb_renderer, False)
		column.pack_start(txt_renderer, True)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(False)
		column.set_attributes(pb_renderer, pixbuf=0)
		column.set_attributes(txt_renderer, markup=1)
		return column
