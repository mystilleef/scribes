from gettext import gettext as _

class Initializer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __set_properties(self):
		from gtk import TreeView, CellRendererToggle, TreeViewColumn
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, CellRendererText
		from gtk import SORT_DESCENDING, SELECTION_MULTIPLE
		view = self.__view
		view.get_selection().set_mode(SELECTION_MULTIPLE)
		# Create a column for selecting encodings.
		column = TreeViewColumn()
		view.append_column(column)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_spacing(12)
		renderer = CellRendererText()
		column.pack_start(renderer, True)
		column.set_attributes(renderer, text=0)
		column.set_resizable(True)
		# Create a column for character encoding.
		column = TreeViewColumn()
		view.append_column(column)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		renderer = CellRendererText()
		# Create the renderer for the Language column
		column.pack_start(renderer, True)
		column.set_attributes(renderer, text=1)
		column.set_resizable(True)
		column.set_spacing(12)
		# Set treeview properties
		view.columns_autosize()
		view.set_model(self.__create_model())
		#view.set_enable_search(True)
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
