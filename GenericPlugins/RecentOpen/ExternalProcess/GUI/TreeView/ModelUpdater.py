from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "model-data", self.__data_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__treeview = manager.gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		self.__data = []
		return

	def __update(self, data):
		self.__treeview.set_model(None)
		self.__model.clear()
		for icon, info, uri in data:
			self.__manager.response()
			self.__model.append([icon, info, uri])
			self.__manager.response()
		self.__treeview.set_model(self.__model)
		self.__manager.emit("updated-model")
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data)
		return False
