class Entry(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-bar", self.__show_cb)
		self.__sigid3 = self.__entry.connect_after("changed", self.__changed_cb)
		self.__sigid4 = self.__entry.connect("activate", self.__activate_cb)
		self.__sigid5 = self.__entry.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid6 = self.__manager.connect("focus-entry", self.__focus_entry_cb)
		self.__sigid7 = self.__manager.connect("hide-menu", self.__focus_entry_cb)
		self.__sigid8 = self.__manager.connect("search", self.__search_cb)
		self.__sigid9 = self.__manager.connect("search-complete", self.__search_complete_cb)
		self.__sigid10 = self.__entry.connect("button-press-event", self.__button_press_event_cb)
		self.__sigid11 = manager.connect("search-mode-flag", self.__search_mode_flag_cb)
		self.__entry.props.sensitive = True
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_widget("Entry")
		self.__findasyoutype = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__entry)
		self.__editor.disconnect_signal(self.__sigid4, self.__entry)
		self.__editor.disconnect_signal(self.__sigid5, self.__entry)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		self.__editor.disconnect_signal(self.__sigid9, self.__manager)
		self.__editor.disconnect_signal(self.__sigid10, self.__entry)
		self.__editor.disconnect_signal(self.__sigid11, self.__manager)
		self.__entry.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		if self.__editor.selection_range > 1: self.__manager.emit("selection-bounds", self.__editor.selection_bounds)
		self.__entry.grab_focus()
		text = self.__entry.get_text()
		self.__manager.emit("search-string", text)
		return False

	def __change_timeout(self):
		text = self.__entry.get_text()
		self.__manager.emit("search-string", text)
		if self.__findasyoutype is False: return False
		self.__manager.emit("search")
		return False

	def __change_idleadd(self):
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(500, self.__change_timeout, priority=9999)
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__change_idleadd, priority=9999)
		return False

	def __activate_cb(self, *args):
		text = self.__entry.get_text()
		if not text: return False
#		self.__manager.emit("search-string", text)
		self.__manager.emit("entry-activated")
		return True

	def __key_press_event_cb(self, entry, event):
		from gtk.gdk import keyval_name, SHIFT_MASK
		keyname = keyval_name(event.keyval)
		ShiftKey = (event.state & SHIFT_MASK)
		Return = (keyname == "Return")
		Escape = (keyname == "Escape")
		if ShiftKey:
			if Return: self.__manager.emit("back-button")
		if Escape: self.__manager.emit("hide-bar")
		return False

	def __focus_entry_cb(self, *args):
		self.__entry.grab_focus()
		return False

	def __search_cb(self, *args):
		if self.__findasyoutype is False: self.__entry.props.sensitive = False
		return False

	def __search_complete_cb(self, *args):
		self.__entry.props.sensitive = True
		return False

	def __button_press_event_cb(self, *args):
		self.__manager.emit("hide-menu")
		return False

	def __search_mode_flag_cb(self, manager, mode):
		self.__findasyoutype = True if mode == "findasyoutype" else False
		return False

	def __precompile_methods(self):
		methods = (self.__changed_cb,)
		self.__editor.optimize(methods)
		return False
