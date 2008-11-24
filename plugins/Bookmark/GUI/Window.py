from gettext import gettext as _
message = _("Bookmarked lines")

class Window(object):
	"""
	This class creates the window for the template editor.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-window", self.__show_cb)
		self.__sigid3 = manager.connect("hide-window", self.__hide_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__window.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.gui.get_widget("Window")
		return

	def __set_properties(self):
		self.__window.set_transient_for(self.__editor.window)
		return

	def __show_window(self):
		self.__editor.response()
		self.__editor.busy()
		self.__window.show_all()
		self.__window.present()
		self.__editor.set_message(message)
		self.__editor.response()
		return

	def __hide_window(self):
		self.__editor.response()
		self.__editor.busy(False)
		self.__window.hide()
		self.__editor.unset_message(message)
		self.__editor.response()
		return

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__window.destroy()
		self = None
		del self
		return

	def __show_cb(self, *args):
		self.__show_window()
		return

	def __hide_cb(self, *args):
		self.__hide_window()
		return

	def __delete_event_cb(self, *args):
		self.__manager.emit("hide-window")
		return True

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide-window")
		return True
