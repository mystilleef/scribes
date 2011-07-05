from SCRIBES.SignalConnectionManager import SignalManager

class SensitivityManager(SignalManager):

	def __init__(self, manager, widget):
		SignalManager.__init__(self)
		self.__init_attributes(manager, widget)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "generate-uris", self.__insensitive_cb)
		self.connect(manager, "generate-uris-for-treenode", self.__insensitive_cb)
		self.connect(manager, "generating-data-for-treeview", self.__insensitive_cb)
		self.connect(manager, "updated-model", self.__sensitive_cb)

	def __init_attributes(self, manager, widget):
		self.__manager = manager
		self.__widget = widget
		return

	def __insensitive_cb(self, *args):
		self.__widget.set_property("sensitive", False)
		return False

	def __sensitive_cb(self, *args):
		self.__widget.set_property("sensitive", True)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
