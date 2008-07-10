class TreeView(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("populate-model", self.__populate_cb)
		self.__sigid3 = self.__treeview.connect("row-activated", self.__row_activated_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__model = self.__create_model()
		self.__line_column = self.__create_line_column()
		self.__text_column = self.__create_text_column()
		self.__treeview = manager.glade.get_widget("TreeView")
		return

	def __set_properties(self):
		self.__treeview.append_column(self.__line_column)
		self.__treeview.append_column(self.__text_column)
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(int, str)
		return model

	def __create_column(self):
		return column

	def __create_line_column(self):
		from gtk import TreeViewColumn, CellRendererText
		from gtk import TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		text_renderer = CellRendererText()
		column.pack_start(text_renderer, False)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(50)
		column.set_resizable(False)
		column.set_attributes(text_renderer, text=0)
		return column

	def __create_text_column(self):
		from gtk import TreeViewColumn, CellRendererText
		from gtk import TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		text_renderer = CellRendererText()
		column.pack_start(text_renderer, False)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(250)
		column.set_resizable(False)
		column.set_attributes(text_renderer, text=1)
		return column

	def __populate_model(self, data):
		try:
			self.__treeview.set_property("sensitive", False)
			self.__treeview.set_model(None)
			self.__model.clear()
			if not data: raise ValueError
			append = self.__model.append
			for line, text in data:
				append([line, text])
			self.__treeview.set_model(self.__model)
			self.__treeview.set_property("sensitive", True)
			self.__treeview.grab_focus()
		except ValueError:
			self.__treeview.set_model(self.__model)
		return False

	def __scroll_to_line(self):
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __populate_cb(self, manager, data):
		self.__populate_model(data)
		return False

	def __row_activated_cb(self, *args):
		self.__scroll_to_line()
		return False
