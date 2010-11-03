from SCRIBES.SignalConnectionManager import SignalManager

class Disabler(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "search-pattern", self.__freeze_cb)
		self.connect(manager, "selected-row", self.__thaw_cb, True)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__is_frozen = False
		self.__treeview = manager.gui.get_object("TreeView")
		return

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

	def __freeze_cb(self, *args):
		self.__treeview.props.sensitive = False
		self.__freeze()
		return False

	def __thaw_cb(self, *args):
		self.__thaw()
		self.__treeview.props.sensitive = True
		return False
