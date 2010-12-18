from gtk.gdk import MODIFIER_MASK
from gtk.keysyms import Tab, Escape, ISO_Left_Tab

from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "inserted-template", self.__unblock_cb, True)
		self.connect(manager, "exit-sparkup-mode", self.__block_cb, True)
		self.__sigid1 = self.connect(editor.textview, "key-press-event", self.__event_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__blocked = False
		from gtk.gdk import keymap_get_default
		self.__keymap = keymap_get_default()
		self.__quit_count = 0
		return

	def __block(self):
		if self.__blocked: return False
		self.__editor.textview.handler_block(self.__sigid1)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__editor.textview.handler_unblock(self.__sigid1)
		self.__blocked = False
		return False

	def __emit(self, signal):
		self.__manager.emit(signal)
		return True

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __event_cb(self, view, event):
		translate = self.__keymap.translate_keyboard_state
		data = translate(event.hardware_keycode, event.state, event.group)
		keyval, egroup, level, consumed = data
		any_on = event.state & ~consumed & MODIFIER_MASK
		# Handle backspace key press event.
		if not any_on and event.keyval == ISO_Left_Tab: return self.__emit("previous-placeholder")
		# Handle delete key press event.
		if not any_on and event.keyval == Tab: return self.__emit("next-placeholder")
		if not any_on and event.keyval == Escape: return self.__emit("exit-sparkup-mode")
		return False

	def __block_cb(self, *args):
		self.__quit_count -= 1
		if self.__quit_count: return False
		self.__block()
		return False

	def __unblock_cb(self, *args):
		self.__quit_count += 1
		self.__unblock()
		return False
