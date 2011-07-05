from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__treeview, "row-expanded", self.__row_expanded_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		return

	def __handle_expansion(self, iterator, path):
		first_child_iterator = self.__model.iter_children(iterator)
		folder_uri = self.__model.get_value(first_child_iterator, 2)
		if folder_uri: return False
		folder_uri = self.__model.get_value(iterator, 2)
		from gtk import TreeRowReference
		treerow_reference = TreeRowReference(self.__model, path)
		self.__model.remove(first_child_iterator)
		from gobject import idle_add
		idle_add(self.__manager.emit, "generate-uris-for-treenode", (folder_uri, treerow_reference))
		return False

	def __row_expanded_cb(self, treeview, iterator, path):
		self.__handle_expansion(iterator, path)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
