class TreeView(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__populate_model()
		self.__select_language()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__editor.connect("loaded-document", self.__generic_cb)
		self.__sigid3 = self.__editor.connect("renamed-document", self.__generic_cb)
		self.__sigid4 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__sigid5 = manager.connect_after("show-window", self.__show_window_cb)
		self.__sigid6 = manager.connect("select-langauge", self.__select_language_cb)
		self.__treeview.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.glade.get_widget("LanguageTreeView")
		self.__is_first_time = True
		self.__model = self.__create_model()
		self.__renderer = self.__create_renderer()
		self.__column = self.__create_column()
		self.__languages = editor.language_ids
		return

	def __set_properties(self):
		from gtk.gdk import ACTION_DEFAULT, BUTTON1_MASK
		from gtk import TARGET_SAME_APP
		self.__treeview.enable_model_drag_source(BUTTON1_MASK, [("STRING", 0, 123)], ACTION_DEFAULT)
		self.__treeview.enable_model_drag_dest([("STRING", TARGET_SAME_APP, 124)], ACTION_DEFAULT)
#		self.__treeview.set_property("rules-hint", True)
#		self.__treeview.set_property("search-column", 0)
#		self.__treeview.set_property("headers-clickable", True)
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
		from gtk import SORT_ASCENDING
		from i18n import msg0001
		column = TreeViewColumn(msg0001, self.__renderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_renderer(self):
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __populate_model(self):
		language_list = self.__editor.language_objects
		language_names = [(name.get_name(), name.get_id()) for name in language_list]
		self.__model.append(["General", "General"])
		for name, id_ in language_names:
			if id_ == "def": continue
			self.__model.append([name, id_])
		return

	def __select_language(self, language=None):
		if not language:
			language_id = self.__get_language()
		else:
			language_id = language
		model = self.__model
		iterator = model.get_iter_first()
		language = model.get_value(iterator, 1)
		if language == language_id:
			selection = self.__treeview.get_selection()
			selection.select_iter(iterator)
			path = model.get_path(iterator)
			self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
		else:
			while True:
				iterator = model.iter_next(iterator)
				if iterator:
					language = model.get_value(iterator, 1)
					if (language == language_id):
						selection = self.__treeview.get_selection()
						selection.select_iter(iterator)
						path = model.get_path(iterator)
						self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
						break
				else:
					break
		self.__treeview.grab_focus()
		self.__manager.emit("language-selected", language_id)
		return

	def __get_language(self):
		language = self.__editor.language
		if not language: return "General"
		return language.get_id()

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__treeview.destroy()
		self = None
		del self
		return

	def __cursor_changed_cb(self, *args):
		try:
			selection = self.__treeview.get_selection()
			model, iterator = selection.get_selected()
			language_id = model.get_value(iterator, 1)
			self.__manager.emit("language-selected", language_id)
		except TypeError:
			pass
		return

	def __show_window_cb(self, *args):
		self.__select_language()
		self.__manager.emit("select-description-view")
		return False

	def __generic_cb(self, *args):
		self.__select_language()
		return

	def __select_language_cb(self, manager, language):
		self.__select_language(language)
		return False
