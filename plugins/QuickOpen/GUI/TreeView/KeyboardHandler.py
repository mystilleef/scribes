class Handler(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__view.connect("key-press-event", self.__event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		from gtk.keysyms import Up, Down, Return, Escape
		self.__dictionary = {
#			Up: self.__select_previous,
#			Down: self.__select_next,
			Return: "row-activated",
			Escape: "hide",
		}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
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
