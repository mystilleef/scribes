from SCRIBES.SignalConnectionManager import SignalManager

class Switcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "gained-focus", self.__gained_focus_cb)
		self.connect(manager, "lost-focus", self.__lost_focus_cb)
		self.connect(manager, "switch-focus", self.__switch_focus_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__is_focused = False
		self.__treeview = manager.gui.get_object("TreeView")
		return

	def __gained_focus_cb(self, *args):
		self.__is_focused = True
		return False

	def __lost_focus_cb(self, *args):
		self.__is_focused = False
		return False

	def __switch_focus_cb(self, *args):
		self.__editor.textview.grab_focus() if self.__is_focused else self.__treeview.grab_focus()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
