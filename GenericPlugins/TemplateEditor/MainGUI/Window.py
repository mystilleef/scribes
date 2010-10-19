class Window(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-window", self.__show_cb)
		self.__sigid3 = manager.connect("hide-window", self.__hide_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.gui.get_widget("Window")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__window.destroy()
		del self
		self = None
		return False

	def __set_properties(self):
		self.__window.set_transient_for(self.__editor.window)
		return False

	def __show(self):
		self.__window.show_all()
		return False

	def __hide(self):
		self.__window.hide()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __hide_cb(self, *args):
		self.__hide()
		return False

	def __show_cb(self, *args):
		self.__show()
		return False

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide-window")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk.keysyms import Escape
		if event.keyval != Escape: return False
		self.__manager.emit("hide-window")
		return True
