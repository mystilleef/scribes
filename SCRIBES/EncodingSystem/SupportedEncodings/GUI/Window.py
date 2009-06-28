class Window(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid3 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid4 = manager.connect("activate", self.__activate_cb)
		self.__window.set_property("sensitive", True)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__window = manager.gui.get_widget("Window")
		return False

	def __set_properties(self):
		self.__window.set_transient_for(self.__editor.window)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__window)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __hide(self):
		self.__window.hide()
		return False

	def __show(self):
		self.__window.show_all()
		return False

	def __delete_event_cb(self, *args):
		self.__hide()
		return True

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__hide()
		return True

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
