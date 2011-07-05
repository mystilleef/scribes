from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate-selection", self.__row_activated_cb)
		self.connect(self.__treeview, "row-activated", self.__row_activated_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		self.__selection = self.__treeview.get_selection()
		return

	def __handle_activation(self):
		model, paths = self.__selection.get_selected_rows()
		if not paths: return False
		folders = [model[path][2] for path in paths if model[path][3] == "folder"]
		files = [model[path][2] for path in paths if model[path][3] == "file"]
		from gobject import idle_add
		if files:
			idle_add(self.__editor.open_files, files)
			idle_add(self.__manager.emit, "activate")
		else:
			if folders: idle_add(self.__manager.emit, "generate-uris", folders[0])
		return False

	def __row_activated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__handle_activation)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
