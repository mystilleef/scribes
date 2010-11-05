from gtk.keysyms import Shift_L, Shift_R, Caps_Lock, BackSpace, Return
from gtk.keysyms import Tab, Delete, Up, Down, Left, Right, Escape
from gtk.keysyms import Alt_L, Alt_R, Control_R, Control_L, U, A, B, C
from gtk.keysyms import D, E, F, i, Num_Lock
from gtk.gdk import CONTROL_MASK, SHIFT_MASK, MODIFIER_MASK
from gtk.gdk import BUTTON_PRESS
from gtk.gdk import keyval_to_unicode

from SCRIBES.SignalConnectionManager import SignalManager

SAFE_KEYS = (
		Shift_L, Shift_R, Alt_L, Alt_R, Control_L, Control_R, Caps_Lock,
		Return, Tab, Num_Lock,
	)

ARROW_KEYS = (Up, Down, Left, Right,)

UNICODE_KEYS = (U, A, B, C, D, E, F, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "deactivate", self.__deactivate_cb)
		self.connect(manager, "inserted-text", self.__inserted_cb)
		self.__sigid1 = self.connect(self.__window, "key-press-event", self.__key_event_cb)
		self.__sigid2 = self.connect(editor.textview, "event", self.__button_event_cb)
		self.__block()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = editor.window
		from gtk.gdk import keymap_get_default
		self.__keymap = keymap_get_default()
		self.__blocked = False
		self.__inserted_text = False
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __block(self):
		if self.__blocked: return False
		self.__window.handler_block(self.__sigid1)
		self.__editor.textview.handler_block(self.__sigid2)
		self.__blocked = True
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__window.handler_unblock(self.__sigid1)
		self.__editor.textview.handler_unblock(self.__sigid2)
		self.__blocked = False
		return False

	def __handle_arrow_keys(self):
		self.__manager.emit("column-mode-reset")
		if self.__inserted_text: self.__manager.emit("clear")
		return False

	def __handle_ctrl_i(self):
		self.__manager.emit("column-mode-reset")
		if self.__inserted_text: self.__manager.emit("clear")
		self.__manager.emit("toggle-edit-point")
		return True

	def __handle_deletion(self, method):
		self.__manager.emit(method)
		return True

	def __toggle_column_edit_point(self, direction):
		if self.__inserted_text: self.__manager.emit("clear")
		self.__manager.emit("column-edit-point", direction)
		return True

	def __keyboard_handler(self, event):
		# Modifier checks
#		from gtk import accelerator_get_default_mod_mask
#		modifier_mask = accelerator_get_default_mod_mask()
		translate = self.__keymap.translate_keyboard_state
		data = translate(event.hardware_keycode, event.state, event.group)
		keyval, egroup, level, consumed = data
		active_mask = any_on = event.state & ~consumed & MODIFIER_MASK
		ctrl_on = active_mask == CONTROL_MASK
		shift_on = active_mask == SHIFT_MASK
		# Handle backspace key press event.
		if not any_on and event.keyval == BackSpace: return self.__handle_deletion("backspace")
		# Handle delete key press event.
		if not any_on and event.keyval == Delete: return self.__handle_deletion("delete")
		# Allow insertion of regular characters into the editing area.
		if not any_on and event.string and keyval_to_unicode(event.keyval): return False
		# Adds column edit points.
		if ctrl_on and event.keyval == Down: return self.__toggle_column_edit_point("down")
		if ctrl_on and event.keyval == Up: return self.__toggle_column_edit_point("up")
		# Allow cursor navigation with arrow keys.
		if event.keyval in ARROW_KEYS: return self.__handle_arrow_keys()
		if event.keyval in SAFE_KEYS: return False
		# Allow insertion of special unicode characters.
		if ctrl_on and shift_on and event.keyval in UNICODE_KEYS: return False
		# Escape exits multi edit mode
		if not any_on and (event.keyval == Escape): return False
		# <ctrl>i adds or removes edit points.
		if ctrl_on and (event.keyval == i): return self.__handle_ctrl_i()
		return True

	def __mouse_handler(self, event):
		view = self.__editor.textview
		window_type = view.get_window_type(event.window)
		position = view.window_to_buffer_coords(window_type, int(event.x), int(event.y))
		iterator = view.get_iter_at_location(*position)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__handle_ctrl_i()
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		self.__unblock()
		return False

	def __deactivate_cb(self, *args):
		self.__block()
		return False

	def __key_event_cb(self, window, event):
		return self.__keyboard_handler(event)

	def __button_event_cb(self, textview, event):
		if event.type == BUTTON_PRESS: return self.__mouse_handler(event)
		return False

	def __inserted_cb(self, manager, inserted):
		self.__inserted_text = inserted
		return False
