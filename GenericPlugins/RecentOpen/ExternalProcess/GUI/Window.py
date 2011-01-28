from SCRIBES.SignalConnectionManager import SignalManager
STARTUP_ID = "ScribesRecentOpenWindow"

class Window(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "show-window", self.__show_cb)
		self.connect(manager, "hide-window", self.__hide_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(self.__window, "delete-event", self.__delete_cb)
		self.connect(self.__window, "key-press-event", self.__key_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__window = manager.gui.get_object("Window")
		return

	def __show(self):
		self.__window.set_startup_id(STARTUP_ID)
		from time import time
		self.__window.present_with_time(int(time()))
		self.__window.window.focus()
		return False

	def __hide(self):
		self.__window.hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __delete_cb(self, *args):
		self.__manager.emit("hide-window")
		return True

	def __key_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__manager.emit("hide-window")
		return True

	def __activate_cb(self, *args):
		self.__manager.emit("show-window")
		return False
