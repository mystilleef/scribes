from SCRIBES.SignalConnectionManager import SignalManager

class Deleter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "delete-row", self.__delete_cb)
		self.connect(self.__treeview, "key-press-event", self.__key_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.main_gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __delete_selected_paths(self):
		try:
			from Utils import get_selected_paths
			paths = get_selected_paths(self.__treeview)
			if not paths: return False
			removable_paths, unremovable_paths = self.__separate(paths)
			if unremovable_paths and not removable_paths: raise ValueError
			if not removable_paths: return False
			self.__treeview.props.sensitive = False
			delete = lambda scheme: self.__manager.emit("remove-scheme", scheme)
			schemes = [self.__model[path][1] for path in removable_paths]
			[delete(scheme) for scheme in schemes]
		except ValueError:
			self.__manager.emit("delete-error")
		return False

	def __separate(self, paths):
		removable_paths = []
		unremovable_paths = []
		for path in paths:
			is_removable = self.__model[path][2]
			removable_paths.append(path) if is_removable else unremovable_paths.append(path)
		return removable_paths, unremovable_paths

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __key_cb(self, window, event):
		from gtk.keysyms import Delete
		if event.keyval != Delete: return False
		self.__manager.emit("delete-row")
		return True

	def __delete_cb(self, *args):
		self.__delete_selected_paths()
		return False
