from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "model-data", self.__data_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.main_gui.get_object("TreeView")
		self.__model = self.__treeview.get_model()
		self.__data = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, data):
#		if self.__data == data: return False
#		from copy import copy
#		self.__data = copy(data)
		self.__treeview.set_model(None)
		self.__model.clear()
		for description, scheme, is_removable in data:
			self.__editor.refresh()
			self.__model.append([description, scheme, is_removable])
		self.__treeview.set_model(self.__model)
		self.__manager.emit("updated-model")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data)
		return False
