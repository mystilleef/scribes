class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		from Window import Window
		Window(manager, editor)
		from TreeView import TreeView
		TreeView(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		manager.emit("populate-model", [(1, "This is a very very very long test line. Yes, it is very long"), (2, "two"), (3, "three"), (4, "four"), (5000, "five")])

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def show(self):
		self.__manager.emit("show-window")
		return
