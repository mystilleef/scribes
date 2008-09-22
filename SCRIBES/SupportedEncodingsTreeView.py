from gettext import gettext as _

class TreeView(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__renderer.connect("toggled", self.__toggled_cb)
		self.__sigid3 = manager.connect("encoding-list", self.__encoding_cb)
		self.__populate_model()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__model = self.__create_model()
		self.__view = manager.glade.get_widget("TreeView")
		from gtk import CellRendererToggle
		self.__renderer = CellRendererToggle()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__renderer)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
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
		view.set_model(self.__model)
		view.columns_autosize()
		#view.set_enable_search(True)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_BOOLEAN
		model = ListStore(TYPE_BOOLEAN, str, str)
		return model

	def __populate_model(self):
		self.__view.set_model(None)
		for encoding, alias, language in self.__editor.supported_encodings:
			self.__model.append([False, encoding, language])
		self.__view.set_model(self.__model)
		return False

	def __update_model(self, encodings):
		self.__view.set_property("sensitive", False)
		self.__view.set_model(None)
		for row in xrange(len(self.__model)):
			treemodelrow = self.__model[row]
			value = True if treemodelrow[1] in encodings else False
			treemodelrow[0] = value
		self.__view.set_model(self.__model)
		self.__view.set_property("sensitive", True)
		self.__view.grab_focus()
		return False

	def __emit_new_encoding(self, path):
		iterator = self.__model.get_iter(path)
		selection = self.__model.get_value(iterator, 0)
		encoding = self.__model.get_value(iterator, 1)
		self.__model.set_value(iterator, 0, not selection)
		selection = self.__model.get_value(iterator, 0)
		self.__manager.emit("new-encoding", encoding, selection)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __toggled_cb(self, renderer, path):
		self.__emit_new_encoding(path)
		return True

	def __encoding_cb(self, manager, encodings):
		self.__update_model(encodings)
		return False
