class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__view.connect("key-press-event", self.__event_cb)
		self.__sigid3 = self.__view.connect("button-press-event", self.__button_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		from gtk.keysyms import Up, Down, Return, Escape
		self.__dictionary = {
			Up: "up-key-press",
			Return: "row-activated",
			Escape: "hide",
		}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__view)
		self.__editor.disconnect_signal(self.__sigid3, self.__view)
		del self
		self = None
		return False

	def __emit(self, signal):
		self.__manager.emit(signal)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __event_cb(self, treeview, event):
		if not (event.keyval in self.__dictionary.keys()): return False
		self.__emit(self.__dictionary[event.keyval])
		return True

	def __button_cb(self, treeview, event):
		from gtk.gdk import _2BUTTON_PRESS
		if event.type != _2BUTTON_PRESS: return False
		self.__manager.emit("row-activated")
		return True

