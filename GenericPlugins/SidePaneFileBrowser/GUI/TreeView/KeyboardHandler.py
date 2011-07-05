from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "showing-browser", self.__show_cb)
		self.connect(manager, "hiding-browser", self.__hide_cb)
		self.connect(manager, "gained-focus", self.__gained_focus_cb)
		self.connect(manager, "lost-focus", self.__lost_focus_cb)
		self.__sigid1 = self.connect(self.__treeview, "key-press-event", self.__treeview_event_cb)
		self.__sigid2 = self.connect(self.__window, "key-press-event", self.__window_event_cb)
		self.__block_treeview_signal()
		self.__block_window_signal()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_object("TreeView")
		self.__window = editor.window
		from gtk import accel_groups_from_object
		self.__accelgroup = accel_groups_from_object(self.__window)[0]
		self.__accel_group_is_removed = False
		self.__treeview_signal_is_blocked = False
		self.__window_signal_is_blocked = False
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __remove_accel_group(self):
		# To avoid keyboard shortcut conflicts remove Scribes default accelerator group when the side pane is active.
		if self.__accel_group_is_removed: return False
		self.__accel_group_is_removed = True
		self.__window.remove_accel_group(self.__accelgroup)
		return False

	def __add_accel_group(self):
		if self.__accel_group_is_removed is False: return False
		self.__accel_group_is_removed = False
		self.__window.add_accel_group(self.__accelgroup)
		return False

	def __block_treeview_signal(self):
		if self.__treeview_signal_is_blocked: return False
		self.__treeview_signal_is_blocked = True
		self.__treeview.handler_block(self.__sigid1)
		return False

	def __unblock_treeview_signal(self):
		if self.__treeview_signal_is_blocked is False: return False
		self.__treeview_signal_is_blocked = False
		self.__treeview.handler_unblock(self.__sigid1)
		return False

	def __block_window_signal(self):
		if self.__window_signal_is_blocked: return False
		self.__window_signal_is_blocked = True
		self.__window.handler_block(self.__sigid2)
		return False

	def __unblock_window_signal(self):
		if self.__window_signal_is_blocked is False: return False
		self.__window_signal_is_blocked = False
		self.__window.handler_unblock(self.__sigid2)
		return False

	def __show_cb(self, *args):
		self.__remove_accel_group()
		self.__unblock_treeview_signal()
		self.__unblock_window_signal()
		return False

	def __hide_cb(self, *args):
		self.__add_accel_group()
		self.__block_window_signal()
		self.__block_treeview_signal()
		return False

	def __gained_focus_cb(self, *args):
		self.__remove_accel_group()
		self.__unblock_treeview_signal()
		return False

	def __lost_focus_cb(self, *args):
		self.__add_accel_group()
		self.__block_treeview_signal()
		return False

	def __emit(self, signal):
		from gobject import idle_add
		idle_add(self.__manager.emit, signal)
		return True

	def __treeview_event_cb(self, treeview, event):
		from gtk.gdk import keyval_name, MOD1_MASK, CONTROL_MASK
		if (event.state == MOD1_MASK) and (keyval_name(event.keyval) == "Left"): return self.__emit("go-back")
		if (event.state == MOD1_MASK) and (keyval_name(event.keyval) == "Up"): return self.__emit("go-up")
		if (event.state == MOD1_MASK) and (keyval_name(event.keyval) == "Home"): return self.__emit("go-home")
		if (event.state == CONTROL_MASK) and (keyval_name(event.keyval) == "h"): return self.__emit("toggle-hidden")
		if (event.state & 0 == 0) and (keyval_name(event.keyval) == "F4"): return self.__emit("activate")
		if (event.state & 0 == 0) and (keyval_name(event.keyval) == "Escape"): return self.__emit("activate")
		if (event.state & 0 == 0) and (keyval_name(event.keyval) == "Return"): return self.__emit("activate-selection")
		return False

	def __window_event_cb(self, window, event):
		from gtk.gdk import keyval_name
		if (event.state & 0 == 0) and (keyval_name(event.keyval) == "F6"): return self.__emit("switch-focus")
		return False
