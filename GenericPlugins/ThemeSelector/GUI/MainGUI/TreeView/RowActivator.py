from SCRIBES.SignalConnectionManager import SignalManager

class Activator(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "ignore-row-activation", self.__ignore_cb)
		self.connect(self.__treeview, "cursor-changed", self.__changed_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__ignore = False
		self.__treeview = manager.main_gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __activate(self):
		self.__editor.refresh(False)
		from Utils import get_selected_paths
		paths = get_selected_paths(self.__treeview)
		if not paths: return False
		scheme = self.__model[paths[0]][1]
		self.__manager.emit("new-scheme", scheme)
		self.__editor.refresh(False)
		return False

	def __activate_timeout(self):
		from gobject import source_remove, idle_add
		self.__timer = idle_add(self.__activate, priority=99999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __ignore_cb(self, manager, ignore):
		self.__ignore = ignore
		return False

	def __changed_cb(self, *args):
		if self.__ignore: return False
		try:
			self.__manager.emit("row-changed")
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(250, self.__activate_timeout, priority=99999)
		return False
