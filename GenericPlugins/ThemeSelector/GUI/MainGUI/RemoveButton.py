from SCRIBES.SignalConnectionManager import SignalManager

class Button(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "last-selected-path", self.__path_cb)
		self.connect(manager, "treeview-sensitivity", self.__sensitive_cb)
		self.connect(manager, "delete-row", self.__delete_cb)
		self.connect(manager, "valid-scheme-files", self.__delete_cb)
		self.connect(self.__button, "clicked", self.__clicked_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.main_gui.get_object("RemoveButton")
		self.__model = manager.main_gui.get_object("TreeView").get_model()
		self.__path = (0,)
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __sensitive(self):
		is_removable = self.__model[self.__path][2]
		self.__button.set_property("sensitive", is_removable)
		return False

	def __path_cb(self, manager, path):
		self.__path = path
		from gobject import idle_add
		idle_add(self.__sensitive)
		return True

	def __clicked_cb(self, *args):
		self.__button.props.sensitive = False
		self.__manager.emit("delete-row")
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return True

	def __sensitive_cb(self, manager, sensitive):
		if sensitive is False: self.__button.props.sensitive = sensitive
		if sensitive: self.__sensitive()
		return False

	def __delete_cb(self, *args):
		self.__button.props.sensitive = False
		return False
