from gettext import gettext as _

class TreeView():

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-window", self.__show_cb)
		self.__sigid3 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__sigid4 = manager.connect("description-treeview-data", self.__populate_cb)
		self.__sigid5 = manager.connect("language-treeview-cursor-changed", self.__clear_cb)
		self.__sigid6 = manager.connect("select-description-treeview", self.__select_cb)
		self.__sigid7 = manager.connect("remove-selected-templates", self.__remove_selected_templates_cb)
		self.__sigid8 = self.__treeview.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid9 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__sigid10 = manager.connect("new-template-data", self.__new_template_data_cb)
		self.__sigid11 = manager.connect("created-template-file", self.__created_file_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_widget("DescriptionTreeView")
		self.__model = self.__create_model()
		self.__column1 = self.__create_name_column()
		self.__column2 = self.__create_description_column()
		self.__selection = self.__treeview.get_selection()
		self.__populate = True
		from gtk.keysyms import Delete, Return
		self.__navigation_dictionary = {
			Delete: self.__remove,
			Return: self.__show_edit,
		}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid9, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid10, self.__manager)
		self.__editor.disconnect_signal(self.__sigid11, self.__manager)
		self.__treeview.destroy()
		del self
		self=None
		return False

	def __populate_model(self, data):
		try:
			if self.__populate is False: raise ValueError
			self.__treeview.handler_block(self.__sigid3)
			self.__sensitive(False)
			self.__treeview.set_model(None)
			self.__model.clear()
			for name, description, key in data:
				self.__model.append([name, description, key])
			self.__treeview.set_model(self.__model)
			self.__update_sensitivity()
			self.__treeview.handler_unblock(self.__sigid3)
			self.__manager.emit("populated-description-treeview")
		except ValueError:
			self.__treeview.grab_focus()
		finally:
			self.__populate = True
		return False

	def __select(self, row, focus=False):
		self.__selection.select_iter(row.iter)
		self.__treeview.set_cursor(row.path, self.__column1)
		self.__treeview.scroll_to_cell(row.path, None, True, 0.5, 0.5)
		if focus: self.__treeview.grab_focus()
		return

	def __select_key(self, key):
		for row_ in self.__model:
			if row_[-1] != key: continue
			path = self.__model.get_path(row_.iter)
			row = self.__model[path]
			self.__select(row, True)
			return
		self.__select(self.__model[0])
		return False

	def __clear(self):
		if not len(self.__model): return False
		self.__treeview.set_model(None)
		self.__model.clear()
		self.__sensitive(False)
		return False

	def __update_sensitivity(self):
		sensitive = True if len(self.__model) else False
		self.__sensitive(sensitive)
		return False

	def __sensitive(self, sensitive):
		self.__treeview.set_property("sensitive", sensitive)
		self.__manager.emit("description-treeview-sensitivity", sensitive)
		return False

	def __emit_template_dictionary_key_async(self):
		try:
			self.__manager.emit("description-treeview-cursor-changed")
			from gobject import timeout_add, source_remove
			source_remove(self.__timer1)
		except AttributeError:
			pass
		finally:
			self.__timer1 = timeout_add(250, self.__emit_template_dictionary_async, priority=9999)
		return False

	def __emit_template_dictionary_async(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer2)
		except AttributeError:
			pass
		finally:
			self.__timer2 = idle_add(self.__emit_key, priority=9999)
		return False

	def __emit_key(self):
		try:
			model, paths = self.__selection.get_selected_rows()
			iterator = model.get_iter(paths[-1])
			key = model.get_value(iterator, 2)
			self.__manager.emit("selected-templates-dictionary-key", key)
		except AttributeError:
			pass
		return False

	def __emit_selected_keys(self):
		model, paths = self.__selection.get_selected_rows()
		get_key = lambda path: model.get_value(model.get_iter(path), 2)
		keys = [get_key(path) for path in paths]
		self.__manager.emit("selected-templates-dictionary-keys", keys)
		return False

	def __remove(self):
		try:
			self.__populate = False
			self.__sensitive(False)
			model, paths = self.__selection.get_selected_rows()
			keys = self.__get_keys(paths)
			self.__manager.emit("remove-template-data", keys)
			self.__remove_keys(keys)
		finally:
			self.__update_sensitivity()
		return False

	def __remove_key(self, key, select):
		for row in self.__model:
			if row[-1] != key: continue
			iterator = row.iter
			success = self.__model.remove(iterator)
			if not select: return False
			if not len(self.__model): return False
			path = self.__model.get_path(iterator) if success else self.__model[-1].path
			row = self.__model[path]
			self.__select(row, True)
		return False

	def __remove_keys(self, keys):
		key = keys[0]
		select = True if len(keys) == 1 else False
		self.__remove_key(key, select)
		keys.remove(key)
		if not keys: return
		return self.__remove_keys(keys)

	def __get_keys(self, paths):
		keys = []
		for path in paths:
			iterator = self.__model.get_iter(path)
			key = self.__model.get_value(iterator, 2)
			keys.append(key)
		return keys

	def __set_properties(self):
		from gtk import SELECTION_MULTIPLE
		self.__selection.set_mode(SELECTION_MULTIPLE)
		from gtk.gdk import BUTTON1_MASK, ACTION_COPY, ACTION_DEFAULT
		targets = [("text/plain", 0, 123), ("STRING", 0, 123)]
		self.__treeview.enable_model_drag_source(BUTTON1_MASK, targets, ACTION_COPY|ACTION_DEFAULT)
		self.__treeview.set_property("model", self.__model)
		self.__treeview.append_column(self.__column1)
		self.__treeview.append_column(self.__column2)
		self.__column1.clicked()
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, str, str)
		return model

	def __create_column(self, name, column):
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import CellRendererText
		column = TreeViewColumn(name, CellRendererText(), text=column)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		return column

	def __create_name_column(self):
		column = self.__create_column(_("_Name"), 0)
		column.set_property("expand", False)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		from gtk import SORT_ASCENDING
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_description_column(self):
		column = self.__create_column(_("_Description"), 1)
		column.set_property("expand", True)
		return column

	def __show_edit(self):
		self.__manager.emit("show-edit-template-editor")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		if len(self.__model): self.__select(self.__model[0], True)
		return False

	def __cursor_changed_cb(self, *args):
		self.__emit_template_dictionary_key_async()
		return False

	def __populate_cb(self, manager, data):
		self.__populate_model(data)
		return False

	def __clear_cb(self, *args):
		self.__clear()
		return False

	def __select_cb(self, manager, key):
		if len(self.__model): self.__select_key(key)
		return False

	def __remove_selected_templates_cb(self, *args):
		self.__remove()
		return False

	def __key_press_event_cb(self, treeview, event):
		if not (event.keyval in self.__navigation_dictionary.keys()): return False
		self.__navigation_dictionary[event.keyval]()
		return True

	def __row_activated_cb(self, *args):
		self.__show_edit()
		return False

	def __created_file_cb(self, *args):
		self.__emit_selected_keys()
		return False

	def __new_template_data_cb(self, *args):
		self.__sensitive(False)
		return False
