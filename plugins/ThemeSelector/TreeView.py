class TreeView(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__sigid3 = self.__treeview.connect_after("cursor-changed", self.__cursor_changed_cb)
		self.__sigid4 = manager.connect("treeview-data", self.__treeview_data_cb)
		self.__sigid5 = manager.connect("current-scheme", self.__current_scheme_cb)
		self.__sigid6 = self.__treeview.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid7 = manager.connect("remove-row", self.__remove_row_cb)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_widget("TreeView")
		self.__model = self.__create_model()
		self.__column = self.__create_column()
		self.__selection = self.__treeview.get_selection()
		self.__current_scheme = None
		self.__can_change_theme = True
		self.__can_populate = True
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__treeview.destroy()
		del self
		self = None
		return False

	def __set_properties(self):
		self.__treeview.append_column(self.__column)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_OBJECT
		model = ListStore(str, TYPE_OBJECT, bool)
		return model

	def __create_column(self):
		from gtk import TreeViewColumn, CellRendererText, TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		renderer = CellRendererText()
		column.pack_start(renderer, False)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(False)
		column.set_attributes(renderer, text=0)
		return column

	def __populate_model(self, data):
		try:
			if self.__can_populate is False: raise ValueError
			self.__can_change_theme = False
			self.__sensitive(False)
			self.__treeview.handler_block(self.__sigid3)
			self.__treeview.set_model(None)
			self.__model.clear()
			for description, scheme, can_remove in data:
				self.__model.append([description, scheme, can_remove])
			self.__treeview.set_model(self.__model)
			self.__treeview.handler_unblock(self.__sigid3)
			from gobject import timeout_add
			timeout_add(100, self.__sensitive, True)
			self.__manager.emit("populated-model")
		except ValueError:
			self.__can_populate = True
		return False

	def __sensitive(self, sensitive=True):
		self.__treeview.set_property("sensitive", sensitive)
		self.__focus_treeview()
		return False

	def __remove(self):
		try:
			self.__sensitive(False)
			self.__can_populate = False
			model, iterator = self.__selection.get_selected()
			can_remove = model.get_value(iterator, 2)
			if can_remove is False: raise TypeError
			scheme = model.get_value(iterator, 1)
			success = model.remove(iterator)
			self.__manager.emit("remove-scheme", scheme)
			if not len(model): raise ValueError
			iterator = iterator if success else model[-1].iter
			scheme = model.get_value(iterator, 1)
			self.__select(scheme)
			self.__sensitive(True)
		except TypeError:
			self.__can_populate = True
			self.__sensitive(True)
		except ValueError:
			self.__can_populate = True
			self.__sensitive(False)
		finally:
			self.__focus_treeview()
		return False

	def __process_cursor_change(self):
		self.__set_theme_async()
		self.__emit_can_remove_signal()
		self.__focus_treeview()
		return False

	def __emit_can_remove_signal(self):
		try:
			model, iterator = self.__selection.get_selected()
			can_remove = model.get_value(iterator, 2)
			self.__manager.emit("remove-button-sensitivity", can_remove)
		except TypeError:
			pass
		return False

	def __set_theme_async(self):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__theme_timer)
		except AttributeError:
			pass
		finally:
			self.__theme_timer = timeout_add(250, self.__set_theme, priority=9999)
		return False

	def __set_theme(self):
		try:
			if self.__can_change_theme is False: raise ValueError
			model, iterator = self.__selection.get_selected()
			scheme = model.get_value(iterator, 1)
			self.__manager.emit("new-scheme", scheme)
		except ValueError:
			pass
		except TypeError:
			print "ERROR: No selection found"
		finally:
			self.__can_change_theme = True
			self.__focus_treeview()
		return False

	def __get_scheme_row(self, scheme):
		row = None
		for _row in self.__model:
			if _row[1].get_id() != scheme.get_id(): continue
			row = _row
			break
		return row

	def __select(self, scheme):
		row = self.__get_scheme_row(scheme)
		self.__selection.select_iter(row.iter)
		self.__treeview.grab_focus()
		self.__treeview.set_cursor(row.path, self.__column)
		self.__treeview.scroll_to_cell(row.path, None, True, 0.5, 0.5)
		self.__focus_treeview()
		return False

	def __focus_treeview(self):
		tv = self.__treeview
		if len(self.__model) and tv.props.sensitive: tv.grab_focus()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __row_activated_cb(self, *args):
		self.__set_theme()
		self.__manager.emit("hide-window")
		return True

	def __cursor_changed_cb(self, *args):
		self.__process_cursor_change()
		return True

	def __treeview_data_cb(self, manager, data):
		self.__populate_model(data)
		return False

	def __current_scheme_cb(self, manager, scheme):
		self.__select(scheme)
		return False

	def __key_press_event_cb(self, treeview, event):
		from gtk import keysyms
		if event.keyval != keysyms.Delete: return False
		self.__remove()
		return True

	def __remove_row_cb(self, *args):
		self.__remove()
		return False
