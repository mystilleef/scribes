class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__init_window_bindings()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid9 = editor.window.connect("scribes-close-window", self.__close_window_cb)
		self.__sigid10 = editor.window.connect("scribes-close-window-nosave", self.__close_window_nosave_cb)
		self.__sigid11 = editor.window.connect("shutdown", self.__shutdown_cb)
		self.__sigid12 = editor.window.connect("fullscreen", self.__fullscreen_cb)
		editor.response()
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid11, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid12, self.__editor.window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __init_window_bindings(self):
		self.__bind_shortcut("ctrl+w", "scribes-close-window")
		self.__bind_shortcut("ctrl+shift+w", "scribes-close-window-nosave")
		self.__bind_shortcut("ctrl+q", "shutdown")
		self.__bind_shortcut("F11", "fullscreen")
		return False

	def __get_keyval(self, shortcut):
		keyname = shortcut.split("+")[-1]
		from gtk.gdk import keyval_from_name
		return keyval_from_name(keyname)

	def __get_modifier(self, shortcut):
		mask = 0
		modifiers = shortcut.split("+")
		from gtk.gdk import MOD1_MASK, SHIFT_MASK, CONTROL_MASK
		if "ctrl" in (modifiers): mask |= CONTROL_MASK
		if "alt" in (modifiers): mask |= MOD1_MASK
		if "shift" in modifiers: mask |= SHIFT_MASK
		return mask

	def __bind_shortcut(self, shortcut, event_name="scribes-key-event"):
		if not shortcut: return False
		keyval = self.__get_keyval(shortcut)
		modifier = self.__get_modifier(shortcut)
		if (keyval, modifier) in self.__editor.get_shortcuts(): return False
		from gtk import binding_entry_add_signal as bind
		bind(self.__editor.window, keyval, modifier, event_name, str, shortcut)
		self.__editor.add_shortcut((keyval, modifier))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __close_window_cb(self, *args):
		self.__editor.close()
		return False

	def __close_window_nosave_cb(self, *args):
		self.__editor.close(False)
		return False

	def __shutdown_cb(self, *args):
		self.__editor.shutdown()
		return False

	def __fullscreen_cb(self, *args):
		self.__editor.toggle_fullscreen()
		return False
