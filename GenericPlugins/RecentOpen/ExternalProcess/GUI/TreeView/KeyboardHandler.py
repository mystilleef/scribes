from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(self.__window, "key-press-event", self.__window_key_cb)
		self.connect(self.__view, "button-press-event", self.__button_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__view = manager.gui.get_object("TreeView")
		self.__window = manager.gui.get_object("Window")
		from gtk.keysyms import Up, Down, Return, Escape
		self.__window_keys = {
			Return: "activate-selected-rows",
			Escape: "hide-window",
			Down: "down-key-press",
			Up: "up-key-press",
		}
		self.__window_shift_keys = {
			Down: "shift-down-key-press",
			Up: "shift-up-key-press",
		}
		return

	def __emit(self, signal):
		self.__manager.emit(signal)
		return False

	def __window_key_cb(self, widget, event):
		if not (event.keyval in self.__window_keys.keys()): return False
		from gtk.gdk import SHIFT_MASK
		shift_on = event.state & SHIFT_MASK
		keys = self.__window_shift_keys if shift_on else self.__window_keys
		self.__emit(keys[event.keyval])
		return True

	def __button_cb(self, treeview, event):
		from gtk.gdk import _2BUTTON_PRESS
		if event.type != _2BUTTON_PRESS: return False
		self.__manager.emit("activate-selected-rows")
		return True
