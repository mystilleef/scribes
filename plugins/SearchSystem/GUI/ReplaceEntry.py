class Entry(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("hide-bar", self.__reset_cb)
		self.__sigid3 = manager.connect("search-string", self.__reset_cb)
		self.__sigid4 = manager.connect("reset", self.__reset_cb)
		self.__sigid5 = manager.connect("found-matches", self.__found_matches_cb)
		self.__sigid6 = manager.connect("focus-replace-entry", self.__focus_entry_cb)
		self.__sigid7 = self.__entry.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid8 = self.__entry.connect("button-press-event", self.__button_press_event_cb)
		self.__sigid9 = self.__entry.connect("activate", self.__activate_cb)
		self.__sigid10 = self.__entry.connect("changed", self.__changed_cb)
		self.__sigid11 = manager.connect("show-replacebar", self.__changed_cb)
		self.__sigid12 = manager.connect("no-search-string", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_widget("ReplaceEntry")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__entry)
		self.__editor.disconnect_signal(self.__sigid8, self.__entry)
		self.__editor.disconnect_signal(self.__sigid9, self.__entry)
		self.__editor.disconnect_signal(self.__sigid10, self.__entry)
		self.__editor.disconnect_signal(self.__sigid11, self.__manager)
		self.__entry.destroy()
		del self
		self = None
		return

	def __emit_replace_string(self):
		string = self.__entry.get_text()
		self.__manager.emit("replace-string", string)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __reset_cb(self, *args):
		self.__entry.props.sensitive = False
		self.__emit_replace_string()
		return False

	def __found_matches_cb(self, manager, matches):
		sensitive = True if matches else False
		self.__entry.props.sensitive = sensitive
		return False

	def __focus_entry_cb(self, *args):
		self.__entry.grab_focus()
		return False

	def __button_press_event_cb(self, *args):
		self.__manager.emit("hide-menu")
		return False

	def __key_press_event_cb(self, entry, event):
		from gtk.gdk import keyval_name, SHIFT_MASK
		keyname = keyval_name(event.keyval)
		if keyname != "Escape": return False
		self.__manager.emit("hide-bar")
		return False

	def __activate_cb(self, *args):
		self.__emit_replace_string()
		self.__manager.emit("replace-entry-activated")
		return False

	def __changed_cb(self, *args):
		self.__emit_replace_string()
		return False
