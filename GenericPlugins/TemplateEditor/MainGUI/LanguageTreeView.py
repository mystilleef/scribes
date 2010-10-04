class TreeView(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__sigid3 = manager.connect("language-treeview-data", self.__populate_cb)
		self.__sigid4 = manager.connect_after("select-language-treeview-id", self.__select_langauge_treeview_id_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_widget("LanguageTreeView")
		self.__model = self.__create_model()
		self.__column = self.__create_column()
		self.__selection = self.__treeview.get_selection()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return False

	def __populate_model(self, data):
		self.__treeview.handler_block(self.__sigid2)
		self.__treeview.set_property("sensitive", False)
		self.__treeview.set_model(None)
		self.__model.clear()
		for language_name, language_id in data:
			self.__model.append([language_name, language_id])
		self.__treeview.set_model(self.__model)
		self.__treeview.set_property("sensitive", True)
		self.__treeview.handler_unblock(self.__sigid2)
		self.__select(self.__get_language_id())
		return False

	def __get_language_id(self):
		if self.__editor.language_object is None: return "General"
		return self.__editor.language_object.get_id()

	def __select(self, language_id):
		row = None
		for _row in self.__model:
			if _row[1] != language_id: continue
			row = _row
			break
		self.__select_row(row)
		return False

	def __select_row(self, row):
		self.__selection.select_iter(row.iter)
		self.__treeview.set_cursor(row.path, self.__column)
		self.__treeview.scroll_to_cell(row.path, None, True, 0.5, 0.5)
		return

	def __emit_language_id_async(self):
		try:
			self.__manager.emit("language-treeview-cursor-changed")
			from gobject import timeout_add, source_remove
			source_remove(self.__timer1)
		except AttributeError:
			pass
		finally:
			self.__timer1 = timeout_add(250, self.__emit_language_async, priority=9999)
		return False

	def __emit_language_async(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer2)
		except AttributeError:
			pass
		finally:
			self.__timer2 = idle_add(self.__emit_language, priority=9999)
		return False

	def __emit_language(self):
		model, iterator = self.__selection.get_selected()
		language_id = model.get_value(iterator, 1)
		self.__manager.emit("selected-language-id", language_id)
		return False

	def __set_properties(self):
		from gtk.gdk import ACTION_DEFAULT, BUTTON1_MASK
		from gtk import TARGET_SAME_APP
		self.__treeview.enable_model_drag_source(BUTTON1_MASK, [("STRING", 0, 123)], ACTION_DEFAULT)
		self.__treeview.enable_model_drag_dest([("STRING", TARGET_SAME_APP, 124)], ACTION_DEFAULT)
		self.__treeview.append_column(self.__column)
		self.__treeview.set_model(self.__model)
		self.__column.clicked()
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __create_column(self):
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING, CellRendererText
		column = TreeViewColumn(_("Language"), CellRendererText(), text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __cursor_changed_cb(self, *args):
		self.__emit_language_id_async()
		return False

	def __populate_cb(self, manager, data):
		self.__populate_model(data)
		return False

	def __select_langauge_treeview_id_cb(self, manager, language_id):
		self.__select(language_id)
		return False
