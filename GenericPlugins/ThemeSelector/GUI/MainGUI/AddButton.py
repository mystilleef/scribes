from SCRIBES.SignalConnectionManager import SignalManager

class Button(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "treeview-sensitivity", self.__sensitive_cb)
		self.connect(manager, "schemes", self.__disable_cb)
		self.connect(manager, "delete-row", self.__disable_cb)
		self.connect(manager, "valid-scheme-files", self.__disable_cb)
		self.connect(self.__button, "clicked", self.__clicked_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.main_gui.get_object("AddButton")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return True

	def __clicked_cb(self, *args):
		self.__manager.emit("show-chooser")
		return True

	def __sensitive_cb(self, manager, sensitive):
		self.__button.props.sensitive = sensitive
		return False

	def __disable_cb(self, *args):
		self.__button.props.sensitive = False
		return False

