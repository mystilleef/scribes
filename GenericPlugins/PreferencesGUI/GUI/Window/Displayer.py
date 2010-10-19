from gettext import gettext as _

class Displayer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show", self.__show_window_cb)
		self.__sigid3 = manager.connect("hide", self.__hide_window_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.gui.get_object("Window")
		return

	def __show(self):
		self.__window.show_all()
		return False

	def __hide(self):
		self.__window.hide()
		return False

	def __destroy(self):
		signals_data = (
			(self.__sigid1, self.__manager),
			(self.__sigid2, self.__manager),
			(self.__sigid3, self.__manager),
			(self.__sigid4, self.__manager),
			(self.__sigid5, self.__window),
		)
		self.__editor.disconnect_signals(signals_data)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __hide_window_cb(self, *args):
		self.__hide()
		return

	def __show_window_cb(self, *args):
		self.__show()
		return

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide")
		return True
