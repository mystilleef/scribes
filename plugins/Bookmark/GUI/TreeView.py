class TreeView(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("populate-model", self.__populate_cb)
		self.__sigid3 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__sigid4 = manager.connect_after("show-window", self.__show_window_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__model = self.__create_model()
		self.__line_column = self.__create_column(True, 0)
		self.__text_column = self.__create_column(False, 1)
		self.__treeview = manager.gui.get_widget("TreeView")
		return

	def __set_properties(self):
		self.__treeview.append_column(self.__line_column)
		self.__treeview.append_column(self.__text_column)
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(int, str)
		return model

	def __create_column(self, resizable, col):
		from gtk import TreeViewColumn, CellRendererText
		from gtk import TREE_VIEW_COLUMN_FIXED, TREE_VIEW_COLUMN_AUTOSIZE
		column = TreeViewColumn()
		text_renderer = CellRendererText()
		column.pack_start(text_renderer, True)
		column.set_reorderable(False)
		column.set_spacing(10)
		column.set_resizable(resizable)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE) if resizable else column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		if not resizable: column.set_fixed_width(250)
		column.set_attributes(text_renderer, text=col)
		return column

	def __select_row(self):
		iterator = self.__model.get_iter_first()
		selection = self.__treeview.get_selection()
		selection.select_iter(iterator)
		self.__treeview.grab_focus()
		return False

	def __populate_model(self, data):
		try:
			self.__treeview.set_property("sensitive", False)
			self.__treeview.set_model(None)
			self.__model.clear()
			if not data: raise ValueError
			append = self.__model.append
			for line, text in data:
				append([line, text])
			self.__line_column.queue_resize()
			self.__text_column.queue_resize()
			self.__treeview.set_model(self.__model)
			self.__treeview.set_property("sensitive", True)
			self.__select_row()
		except ValueError:
			self.__treeview.set_model(self.__model)
		return False

	def __scroll_to_line(self):
		selection = self.__treeview.get_selection()
		model, iterator = selection.get_selected()
		line = model.get_value(iterator, 0) - 1
		self.__manager.emit("scroll-to-line", line)
		self.__manager.emit("hide-window")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __populate_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__populate_model, data, priority=9999)
		return False

	def __show_window_cb(self, *args):
		self.__treeview.grab_focus()
		return False

	def __row_activated_cb(self, *args):
		self.__scroll_to_line()
		return False
