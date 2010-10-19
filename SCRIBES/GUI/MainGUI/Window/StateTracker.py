class Tracker(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__editor.set_data("minimized", False)
		self.__editor.set_data("maximized", False)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__window.connect("window-state-event", self.__state_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.window
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, state):
		from gtk.gdk import WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN
		from gtk.gdk import WINDOW_STATE_ICONIFIED
		MINIMIZED = state & WINDOW_STATE_ICONIFIED
		MAXIMIZED = (state & WINDOW_STATE_MAXIMIZED) or (state & WINDOW_STATE_FULLSCREEN)
		minimized = True if MINIMIZED else False
		maximized = True if MAXIMIZED else False
		self.__editor.set_data("minimized", minimized)
		self.__editor.set_data("maximized", maximized)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __state_cb(self, window, event):
		from gobject import idle_add
		idle_add(self.__update, event.new_window_state)
		return False
