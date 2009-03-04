class Window(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid2 = editor.connect("close", self.__close_cb)
		self.__sigid3 = self.__window.connect_after("focus-out-event", self.__focus_out_event_cb)
		self.__window.set_property("sensitive", True)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.window
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__window)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		self.__add_signal()
		from gtk import AccelGroup
		self.__window.add_accel_group(AccelGroup())
		from gtk.gdk import KEY_PRESS_MASK
		self.__window.add_events(KEY_PRESS_MASK)
		get_resolution = self.__editor.calculate_resolution_independence
		width, height = get_resolution(self.__window, 1.462857143, 1.536)
		self.__window.set_property("default-height", height)
		self.__window.set_property("default-width", width)
		return

	def __add_signal(self):
		# Add new signal to window.
		from gobject import signal_new, signal_query, SIGNAL_RUN_LAST
		from gobject import TYPE_STRING, TYPE_BOOLEAN, SIGNAL_ACTION
		from gobject import SIGNAL_NO_RECURSE, type_register
		SIGNAL = SIGNAL_ACTION|SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE
		from gtk import Window
		if signal_query("scribes-key-event", Window): return False
		signal_new("scribes-key-event", Window, SIGNAL_ACTION, None, ())
		signal_new("scribes-close-window", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
		signal_new("scribes-close-window-nosave", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
		signal_new("shutdown", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
		signal_new("fullscreen", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
		type_register(type(self.__window))
		return False

	def __delete_event_cb(self, *args):
		self.__editor.close()
		return True

	def __close_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __focus_out_event_cb(self, *args):
		self.__editor.emit("window-focus-out")
		return False