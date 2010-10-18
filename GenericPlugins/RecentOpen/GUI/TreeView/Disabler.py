from SCRIBES.SignalConnectionManager import SignalManager

class Disabler(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "search-pattern", self.__freeze_cb)
		self.connect(manager, "selected-row", self.__thaw_cb, True)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__is_frozen = False
		self.__treeview = manager.gui.get_object("TreeView")
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

	def __freeze_cb(self, *args):
		self.__treeview.props.sensitive = False
#		self.__editor.refresh()
		self.__freeze()
		return False

	def __thaw_cb(self, *args):
		self.__thaw()
		self.__treeview.props.sensitive = True
#		self.__editor.refresh()
		return False
