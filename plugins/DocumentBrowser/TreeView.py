from gettext import gettext as _

class TreeView(object):
	"""
	This class creates a treeview for the bookmark browser.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__manager.connect("update", self.__update_cb)
		self.__sigid3 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__sigid4 = self.__treeview.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.glade.get_widget("TreeView")
		self.__data = None
		self.__model = self.__create_model()
		self.__name_renderer = self.__create_renderer()
		self.__type_renderer = self.__create_renderer()
		self.__path_renderer = self.__create_renderer()
		self.__name_column = self.__create_column(_("File _Name"), self.__name_renderer, 0, False, True)
		self.__type_column = self.__create_column(_("File _Type"), self.__type_renderer, 1, False, True)
		self.__path_column = self.__create_column(_("File _Path"), self.__path_renderer, 2, False, True)
		return

	def __set_properties(self):
		self.__treeview.set_property("model", self.__model)
		self.__treeview.set_property("rules-hint", True)
		self.__treeview.set_property("search-column", 0)
		self.__treeview.set_property("headers-clickable", True)
		self.__treeview.append_column(self.__name_column)
		self.__treeview.append_column(self.__type_column)
		self.__treeview.append_column(self.__path_column)
		self.__name_column.clicked()
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, str, str, str)
		return model

	def __create_renderer(self):
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_column(self, title, renderer, text=0, expand=False, indicator=False):
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, SORT_DESCENDING
		from gtk import TreeViewColumn
		column = TreeViewColumn(title, renderer, text=text)
		column.set_expand(expand)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_indicator(indicator)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(text)
		return column

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __update_cb(self, manager, data):
		if self.__data == data: return False
		from copy import copy
		self.__data = copy(data)
		from gobject import idle_add
		idle_add(self.__populate_model, data, priority=9999)
		return False

	def __populate_model(self, data):
		self.__treeview.set_property("sensitive", False)
		self.__treeview.set_model(None)
		self.__model.clear()
		for type_, name, path, uri in data:
			self.__model.append([name, type_, path, uri])
		self.__treeview.set_model(self.__model)
		self.__editor.select_row(self.__treeview)
		self.__treeview.set_property("sensitive", True)
		self.__treeview.grab_focus()
		return

	def __row_activated_cb(self, treeview, path, column):
		self.__manager.emit("hide-window")
		iterator = self.__model.get_iter(path)
		uri = self.__model.get_value(iterator, 3)
		self.__editor.focus_file(uri)
		return False

	def __key_press_event_cb(self, treeview, event):
		from gtk import keysyms
		if event.keyval != keysyms.Delete: return False
		selection = treeview.get_selection()
		model, iterator = selection.get_selected()
		if not iterator: return False
		uri = model.get_value(iterator, 3)
		model.remove(iterator)
		self.__editor.select_row(self.__treeview)
		self.__editor.close_file(uri)
		return False
