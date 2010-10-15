from SCRIBES.SignalConnectionManager import SignalManager

class Window(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "show-window", self.__show_cb)
		self.connect(manager, "hide-window", self.__hide_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(self.__window, "delete-event", self.__delete_cb)
		self.connect(self.__window, "key-press-event", self.__key_cb)
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.main_gui.get_object("Window")
		return

	def __set_properties(self):
		self.__window.set_transient_for(self.__editor.window)
		return

	def __show(self):
		self.__window.show_all()
		return False

	def __hide(self):
		self.__window.hide()
		return False

	def __destroy(self):
		self.disconnect()
		self.__window.destroy()
		del self
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __show_cb(self, *args):
		self.__show()
		return

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

