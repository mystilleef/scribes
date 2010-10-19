from SCRIBES.SignalConnectionManager import SignalManager

class Disabler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "schemes", self.__updated_cb)
		self.connect(manager, "valid-scheme-files", self.__updated_cb)
		self.connect(manager, "selected-row", self.__selected_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__is_frozen = False
		self.__treeview = manager.main_gui.get_object("TreeView")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __freeze(self):
		if self.__is_frozen: return False
		self.__is_frozen = True
		self.__treeview.window.freeze_updates()
		return False

	def __thaw(self):
		if self.__is_frozen is False: return False
		self.__is_frozen = False
		self.__treeview.window.thaw_updates()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_cb(self, *args):
		self.__manager.emit("treeview-sensitivity", False)
		self.__treeview.grab_focus()
		self.__treeview.props.sensitive = False
		self.__freeze()
		return False

	def __selected_cb(self, *args):
		self.__thaw()
		self.__treeview.props.sensitive = True
		self.__treeview.grab_focus()
		self.__manager.emit("treeview-sensitivity", True)
		return False
