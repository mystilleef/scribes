from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__window, "key-press-event", self.__window_key_cb)
		self.connect(self.__view, "button-press-event", self.__button_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
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

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __emit(self, signal):
		self.__manager.emit(signal)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
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
