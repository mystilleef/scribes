from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "treeview-model-data", self.__data_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		self.__treenode_update = False
		return

	def __update(self, data):
		folders, files, rowref = data
		get_root_iter = lambda rowref: self.__model.get_iter(rowref.get_path())
		self.__treeview.set_model(None)
		if rowref is None: self.__model.clear()
		root_iterator = get_root_iter(rowref) if rowref else self.__model.get_iter_root()
		for uri, display_name, icon, file_type in folders:
			self.__editor.refresh()
			parent_iterator = self.__model.append(root_iterator, [icon, display_name, uri, file_type])
			self.__model.append(parent_iterator, (None,None,None,None))
			if rowref: root_iterator = get_root_iter(rowref)
		for uri, display_name, icon, file_type in files:
			self.__editor.refresh()
			self.__model.append(root_iterator, [icon, display_name, uri, file_type])
			if rowref: root_iterator = get_root_iter(rowref)
		self.__treeview.set_model(self.__model)
		if rowref: self.__treeview.expand_to_path(rowref.get_path())
		self.__treeview.columns_autosize()
		self.__manager.emit("updated-model")
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data)
		return False
