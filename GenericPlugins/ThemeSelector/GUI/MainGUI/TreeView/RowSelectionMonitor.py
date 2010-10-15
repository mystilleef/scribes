from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__treeview, "cursor-changed", self.__changed_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.main_gui.get_object("TreeView")
		self.__selection = self.__treeview.get_selection()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __path(self):
		from Utils import get_selected_paths
		paths = get_selected_paths(self.__treeview)
		if not paths: return False
		self.__manager.emit("last-selected-path", paths[0])
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__path()
		return False
