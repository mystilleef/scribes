from SCRIBES.SignalConnectionManager import SignalManager

class Activator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate-selected-rows", self.__activate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__ignore = False
		self.__treeview = manager.gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate(self):
		from Utils import get_selected_paths
		paths = get_selected_paths(self.__treeview)
		self.__manager.emit("hide-window")
		if not paths: return False
		files = [self.__model[path][2] for path in paths]
		self.__manager.emit("open-files", files)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False
