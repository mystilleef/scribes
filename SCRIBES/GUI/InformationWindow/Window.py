class Window(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("show-error", self.__show_info_cb)
		self.__sigid3 = editor.connect("show-info", self.__show_info_cb)
		self.__sigid4 = manager.connect("hide", self.__hide_cb)
		self.__sigid5 = manager.connect("show", self.__show_cb)
		self.__sigid6 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid7 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__window = manager.gui.get_widget("Window")
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__window)
		self.__editor.disconnect_signal(self.__sigid7, self.__window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __show_window(self, window):
		self.__window.set_transient_for(window)
		self.__manager.emit("show")
		return False

	def __show(self):
		self.__editor.response()
		self.__window.show_all()
		self.__editor.response()
		return False

	def __hide(self):
		self.__editor.response()
		self.__window.hide_all()
		self.__editor.response()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show, priority=9999)
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide, priority=9999)
		return False

	def __show_info_cb(self, editor, title, message, window, busy):
		from gobject import idle_add
		idle_add(self.__show_window, window, priority=9999)
		return False

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide")
		return True

	def __quit_cb(self, *args):
		self.__destroy()
		return False
