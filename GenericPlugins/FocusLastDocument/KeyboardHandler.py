from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor.window, "key-press-event", self.__event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from gtk.gdk import keymap_get_default
		self.__keymap = keymap_get_default()
		return

	def __switch(self):
		self.__manager.emit("switch")
		return True

	def __event_cb(self, window, event):
		translate = self.__keymap.translate_keyboard_state
		data = translate(event.hardware_keycode, event.state, event.group)
		keyval, egroup, level, consumed = data
		from gtk.gdk import MODIFIER_MASK, CONTROL_MASK
		active_mask = event.state & ~consumed & MODIFIER_MASK
		ctrl_on = active_mask == CONTROL_MASK
		from gtk.keysyms import Tab
		if ctrl_on and keyval == Tab: return self.__switch()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
