from gettext import gettext as _

class Window(object):
	"""
	This class creates the window for the document browser window.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__manager.connect("show-window", self.__show_window_cb)
		self.__sigid3 = self.__manager.connect("hide-window", self.__hide_window_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__window.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.glade.get_widget("Window")
		return

	def __set_properties(self):
		width, height = self.__editor.calculate_resolution_independence(self.__editor.window, 1.6, 2.5)
		self.__window.set_property("default-width", width)
		self.__window.set_property("default-height", height)
		self.__window.set_transient_for(self.__editor.window)
		return

	def __show(self):
		self.__window.show_all()
		self.__editor.busy()
		self.__editor.set_message(_("Select document"), "open")
		return

	def __hide(self):
		self.__window.hide()
		self.__editor.busy(False)
		self.__editor.unset_message(_("Select document"), "open")
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
		self.__hide()
		return True

	def __key_press_event_cb(self, window, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__hide()
		return True
