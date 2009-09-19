class Window(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show", self.__show_cb)
		self.__sigid3 = manager.connect("hide", self.__hide_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid6 = manager.connect("current-path", self.__path_cb)
		self.__sigid7 = manager.connect("files", self.__files_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__window = manager.gui.get_object("Window")
		return False

	def __set_properties(self):
		self.__window.set_transient_for(self.__editor.window)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__window.destroy()
		del self
		self = None
		return False

	def __hide(self):
		self.__editor.response()
		self.__window.hide()
		self.__editor.response()
		return False

	def __show(self):
		self.__editor.response()
		self.__window.show_all()
		self.__editor.response()
		return False

	def __change_path(self):
		self.__manager.emit("parent-path")
		return True

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk.gdk import MOD1_MASK
		from gtk.keysyms import Up, Escape
		if event.state & MOD1_MASK and event.keyval == Up: return self.__change_path()
		if event.keyval != Escape: return False
		self.__manager.emit("hide")
		return True

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __files_cb(self, *args):
		self.__window.set_property("sensitive", True)
		return False
	
	def __path_cb(self, *args):
		self.__window.set_property("sensitive", False)
		return False
