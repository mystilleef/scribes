from gettext import gettext as _

class Initializer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_widget("TreeView")
		from ActiveEncodingRenderer import Renderer
		self.__renderer = Renderer(manager, editor)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		from gtk import TreeView, CellRendererToggle, TreeViewColumn
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, CellRendererText
		from gtk import SORT_DESCENDING
		view = self.__view
		self.__renderer.set_property("activatable", True)
		# Create a column for selecting encodings.
		column = TreeViewColumn(_("Select"), self.__renderer)
		view.append_column(column)
		column.set_expand(False)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.add_attribute(self.__renderer, "active", 0)
		column.set_sort_indicator(True)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(0)
		# Create a renderer for the character encoding column.
		renderer = CellRendererText()
		# Create a column for character encoding.
		column = TreeViewColumn(_("Character Encoding"), renderer, text=1)
		view.append_column(column)
		column.set_expand(True)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_indicator(True)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(1)
		# Create the renderer for the Language column
		renderer = CellRendererText()
		# Create a column for Language and Region and set the column's properties.
		column = TreeViewColumn(_("Language and Region"), renderer, text=2)
		view.append_column(column)
		column.set_expand(True)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_indicator(True)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(2)
		# Set treeview properties
		view.columns_autosize()
		view.set_model(self.__create_model())
		#view.set_enable_search(True)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_BOOLEAN
		model = ListStore(TYPE_BOOLEAN, str, str)
		return model

	def __quit_cb(self, *args):
		self.__destroy()
		return False
