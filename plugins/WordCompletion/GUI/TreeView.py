class TreeView(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = self.__view.connect("key-press-event", self.__key_press_event_cb)
		self.__block_view()
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("match-found", self.__match_found_cb)
		self.__sigid4 = manager.connect("no-match-found", self.__no_match_found_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=8888)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__blocked = False
		self.__view = editor.textview
		self.__model = self.__create_model()
		self.__column = self.__create_column()
		self.__treeview = manager.gui.get_widget("TreeView")
		self.__selection = self.__treeview.get_selection()
		self.__matches = []
		from gtk.keysyms import Up, Down, Return, Escape
		self.__navigation_dictionary = {
			Up: self.__select_previous,
			Down: self.__select_next,
			Return: self.__activate_selection,
			Escape: self.__hide,
		}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid1, self.__view)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__treeview.destroy()
		del self
		self = None
		return False

	def __block_view(self):
		if self.__blocked: return
		self.__view.handler_block(self.__sigid1)
		self.__blocked = True
		return

	def __unblock_view(self):
		if self.__blocked is False: return
		self.__view.handler_unblock(self.__sigid1)
		self.__blocked = False
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str)
		return model

	def __create_column(self):
		from gtk import TreeViewColumn, CellRendererText, TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		renderer = CellRendererText()
		column.pack_start(renderer, False)
		column.set_attributes(renderer, text=0)
		column.set_expand(False)
		return column

	def __set_properties(self):
		self.__treeview.append_column(self.__column)
		return False

	def __populate_model(self, matches):
		try:
			if self.__matches == matches: raise ValueError
			self.__treeview.set_model(None)
			self.__model.clear()
			for word in matches: 
				self.__editor.response()
				self.__model.append([word])
			self.__treeview.set_model(self.__model)
			self.__column.queue_resize()
			self.__treeview.columns_autosize()
		except ValueError:
			pass
		finally:
			self.__select(self.__model[0])
			self.__manager.emit("treeview-size", (self.__treeview.size_request()))
			from copy import copy
			self.__matches = copy(matches)
		return False

	def __select(self, row):
		self.__selection.select_iter(row.iter)
		self.__treeview.set_cursor(row.path, self.__column)
		self.__treeview.scroll_to_cell(row.path, None, True, 0.5, 0.5)
		return

	def __select_next(self):
		model, iterator = self.__selection.get_selected()
		iterator = model.iter_next(iterator)
		path = model.get_path(iterator) if iterator else 0
		self.__select(model[path])
		return False

	def __select_previous(self):
		model, iterator = self.__selection.get_selected()
		path = model.get_path(iterator)[0] - 1
		self.__select(model[path])
		return False

	def __activate_selection(self):
		model, iterator = self.__selection.get_selected()
		text = model.get_value(iterator, 0)
		self.__manager.emit("insert-text", text)
		self.__manager.emit("hide-window")
		return False

	def __hide(self):
		self.__manager.emit("no-match-found")
		return False

	def __get_treeview_size(self):
		width, height = self.__treeview.size_request()
		if width < 200: width = 210
		height = 210 if height > 200 else (height + 6)
		width = 210 if width < 200 else width
		return width, height

	def __precompile_methods(self):
		methods = (self.__populate_model, self.__get_treeview_size,
			self.__select, self.__activate_selection)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __match_found_cb(self, manager, matches):
		self.__unblock_view()
		self.__populate_model(matches)
		return False

	def __key_press_event_cb(self, textview, event):
		if not (event.keyval in self.__navigation_dictionary.keys()): return False
		self.__navigation_dictionary[event.keyval]()
		return True

	def __no_match_found_cb(self, *args):
		self.__block_view()
		return False
