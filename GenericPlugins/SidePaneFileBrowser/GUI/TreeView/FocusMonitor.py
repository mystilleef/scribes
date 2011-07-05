from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__treeview, "focus-in-event", self.__focus_in_cb)
		self.connect(self.__treeview, "focus-out-event", self.__focus_out_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_object("TreeView")
		self.__container = manager.gui.get_object("BrowserContainer1")
		return

	def __focus_in_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__manager.emit, "gained-focus")
		return False

	def __focus_out_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__manager.emit, "lost-focus")
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
