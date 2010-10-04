class TreeView(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("dictionary", self.__dictionary_cb)
		self.__sigid3 = self.__abvrenderer.connect("edited", self.__abvedited_cb)
		self.__sigid4 = self.__rplrenderer.connect("edited", self.__rpledited_cb)
		self.__sigid5 = self.__model.connect("row-changed", self.__row_changed_cb)
		self.__sigid6 = manager.connect("show-window", self.__show_cb)
		self.__sigid7 = manager.connect("hide-window", self.__hide_cb)
		self.__sigid8 = self.__treeview.connect("key-press-event", self.__event_cb)
		self.__sigid9 = manager.connect("add-row", self.__add_row_cb)
		self.__sigid10 = manager.connect("edit-row", self.__edit_row_cb)
		self.__sigid11 = manager.connect("delete-row", self.__delete_row_cb)
		self.__sigid12 = self.__treeview.connect("button-press-event", self.__button_press_event_cb)
		self.__sigid13 = self.__abvrenderer.connect("editing-started", self.__editing_started_cb)
		self.__sigid14 = self.__rplrenderer.connect("editing-started", self.__editing_started_cb)
		self.__sigid15 = self.__abvrenderer.connect("editing-canceled", self.__editing_canceled_cb)
		self.__block_row_changed_signal()
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__model = self.__create_model()
		self.__treeview = manager.gui.get_widget("TreeView")
		self.__abvrenderer = self.__create_renderer()
		self.__rplrenderer = self.__create_renderer()
		self.__abvcolumn = self.__create_abbreviation_column()
		self.__rplcolumn = self.__create_replacement_column()
		self.__update = True
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__abvrenderer)
		self.__editor.disconnect_signal(self.__sigid4, self.__rplrenderer)
		self.__editor.disconnect_signal(self.__sigid5, self.__model)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid9, self.__manager)
		self.__editor.disconnect_signal(self.__sigid10, self.__manager)
		self.__editor.disconnect_signal(self.__sigid11, self.__manager)
		self.__editor.disconnect_signal(self.__sigid12, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid13, self.__abvrenderer)
		self.__editor.disconnect_signal(self.__sigid14, self.__rplrenderer)
		self.__editor.disconnect_signal(self.__sigid15, self.__abvrenderer)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __get_string(self, path, column):
		iterator = self.__model.get_iter(path)
		return self.__model.get_value(iterator, column)

	def __exists(self, text):
		for row in self.__model:
			self.__editor.response()
			if text == self.__model.get_value(row.iter, 0): return True
		return False

	def __validate(self, text):
		message = None
		from gettext import gettext as _
		if (" " in text) or ("\t" in text): message = _("Error: Abbreviation must not contain whitespace")
		if self.__exists(text): message = _("Error: '%s' already exists") % text
		if message is None: return False
		self.__manager.emit("error", message)
		raise ValueError
		return False

	def __block_row_changed_signal(self):
		self.__model.handler_block(self.__sigid5)
		return False

	def __unblock_row_changed_signal(self):
		self.__model.handler_unblock(self.__sigid5)
		return False

	def __process_abvrenderer(self, path, text):
		try:
			from Exceptions import DeleteError, DoNothingError
			if not text: raise DeleteError
			string = self.__get_string(path, 0)
			if string == text: raise DoNothingError
			self.__validate(text)
			self.__model[path][0] = text
			self.__edit(path, 1)
		except ValueError:
			self.__edit(path, 0)
		except DeleteError:
			self.__delete()
		except DoNothingError:
			self.__manager.emit("add-button-sensitivity", True)
			self.__check_sensitivity()
		return False

	def __process_rplrenderer(self, path, text):
		self.__model[path][1] = text
		return False

	def __process_row(self, path, iterator):
		try:
			model = self.__model
			get_value = lambda column: model.get_value(iterator, column)
			key, value = get_value(0), get_value(1)
			from Exceptions import EmptyKeyError
			if not key: raise EmptyKeyError
			self.__manager.emit("update-dictionary", (key, value, True))
			self.__update = False
		except EmptyKeyError:
			self.__delete(path)
		finally:
			self.__manager.emit("add-button-sensitivity", True)
			self.__check_sensitivity()
		return False

	def __select_row_at_mouse(self, event):
		try:
			x, y = self.__treeview.widget_to_tree_coords(int(event.x), int(event.y))
			path = self.__treeview.get_path_at_pos(x, y)[0]
			selection = self.__treeview.get_selection()
			selection.select_iter(self.__model.get_iter(path))
			self.__treeview.set_cursor(path, self.__abvcolumn)
			self.__treeview.grab_focus()
		except TypeError:
			pass
		return False

	def __get_path(self):
		try:
			selection = self.__treeview.get_selection()
			model, iterator = selection.get_selected()
		except TypeError:
			raise ValueError
		return model.get_path(iterator)

	def __add(self):
		self.__manager.emit("add-button-sensitivity", False)
		self.__sensitive(True)
		iterator = self.__model.append()
		path = self.__model.get_path(iterator)
		self.__edit(path, 0)
		return False

	def __edit(self, path=None, column=0):
		try:
			self.__manager.emit("add-button-sensitivity", False)
			path = path if path else self.__get_path()
			column = self.__treeview.get_column(column)
			self.__treeview.set_cursor(path, column, start_editing=True)
		except ValueError:
			print "No selection found"
		return False

	def __get_last_iterator(self):
		if not len(self.__model): raise ValueError
		return self.__model[-1].iter

	def __get_selected_iterator(self):
		try:
			selection = self.__treeview.get_selection()
			model, iterator = selection.get_selected()
		except TypeError:
			iterator = None
		return iterator

	def __delete(self, path=None):
		try:
			from Exceptions import NoSelectionFoundError
			model = self.__model
			iterator = model.get_iter(path) if path else self.__get_selected_iterator()
			if not iterator: raise NoSelectionFoundError
			key = model.get_value(iterator, 0)
			value = model.get_value(iterator, 1)
			is_valid = model.remove(iterator)
			if key: self.__update = False
			if key: self.__manager.emit("update-dictionary", (key, value, False))
			if is_valid is False: iterator =  self.__get_last_iterator()
			self.__treeview.get_selection().select_iter(iterator)
			path = self.__model.get_path(iterator)
			self.__treeview.set_cursor(path, self.__abvcolumn)
			self.__treeview.grab_focus()
		except NoSelectionFoundError:
			from gettext import gettext as _
			print _("No selection found")
		except ValueError:
			self.__check_sensitivity()
		finally:
			self.__manager.emit("add-button-sensitivity", True)
		return False

	def __check_sensitivity(self):
		sensitive = True if len(self.__model) else False
		self.__sensitive(sensitive)
		if sensitive: self.__treeview.grab_focus()
		return False

	def __sensitive(self, sensitive=True):
		self.__treeview.set_property("sensitive", sensitive)
		self.__manager.emit("sensitive", sensitive)
		return False

	def __set_properties(self):
		self.__treeview.set_property("model", self.__model)
		self.__treeview.append_column(self.__abvcolumn)
		self.__treeview.append_column(self.__rplcolumn)
		return

	def __populate_model(self, dictionary):
		self.__sensitive(False)
		self.__treeview.set_model(None)
		self.__model.clear()
		for abbreviation, text in dictionary.items():
			self.__editor.response()
			self.__model.append([abbreviation, text])
		self.__treeview.set_model(self.__model)
		if len(self.__model): self.__editor.select_row(self.__treeview)
		self.__check_sensitivity()
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __create_renderer(self):
		from gtk import CellRendererText
		renderer = CellRendererText()
		renderer.set_property("editable", True)
		return renderer

	def __create_abbreviation_column(self):
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from gettext import gettext as _
		column = TreeViewColumn(_("Abbreviation"), self.__abvrenderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_replacement_column(self):
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from gettext import gettext as _
		message = _("Expanded Text")
		column = TreeViewColumn(message, self.__rplrenderer, text=1)
		column.set_property("expand", True)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		return column

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __dictionary_cb(self, manager, dictionary):
		if self.__update: self.__populate_model(dictionary)
		self.__update = True
		return False

	def __abvedited_cb(self, renderer, path, text, *args):
		self.__process_abvrenderer(path, text)
		return False

	def __rpledited_cb(self, renderer, path, text, *args):
		self.__process_rplrenderer(path, text)
		return False

	def __row_changed_cb(self, model, path, iterator, *args):
		self.__process_row(path, iterator)
		return False

	def __show_cb(self, *args):
		self.__unblock_row_changed_signal()
		self.__treeview.grab_focus()
		return False

	def __hide_cb(self, *args):
		self.__block_row_changed_signal()
		self.__treeview.grab_focus()
		return False

	def __event_cb(self, treeview, event):
		from gtk import keysyms
		if event.keyval != keysyms.Delete: return False
		self.__delete()
		return True

	def __edit_row_cb(self, *args):
		self.__edit()
		return False

	def __add_row_cb(self, *args):
		self.__add()
		return False

	def __delete_row_cb(self, *args):
		self.__delete()
		return False

	def __button_press_event_cb(self, treeview, event, *args):
		self.__select_row_at_mouse(event)
		return True

	def __editing_started_cb(self, *args):
		self.__manager.emit("add-button-sensitivity", False)
		return False

	def __editing_canceled_cb(self, *args):
		self.__process_row(self.__get_path(), self.__get_selected_iterator())
		return False
