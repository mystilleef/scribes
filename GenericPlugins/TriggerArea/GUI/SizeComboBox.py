from SCRIBES.SignalConnectionManager import SignalManager

class ComboBox(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_attributes()
		self.__update_model()
		self.__sigid1 = self.connect(self.__combo, "changed", self.__changed_cb)
		self.connect(manager, "configuration-data", self.__update_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__widget = manager.get_data("TriggerWidget")
		self.__model = self.__create_model()
		self.__combo = manager.gui.get_object("SizeComboBox")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, int)
		return model

	def __set_attributes(self):
		from gtk import CellRendererText
		cell = CellRendererText()
		self.__combo.pack_start(cell, True)
		self.__combo.add_attribute(cell, 'text', 0)
		return False

	def __update_model(self):
		data = (
			("small", 24),
			("medium", 32),
			("large", 48),
			("very large", 64),
			("extra large", 128),
		)
		self.__combo.set_model(None)
		for position in data:
			self.__model.append([position[0], position[1]])
		self.__combo.set_model(self.__model)
		return False

	def __set_active(self, size):
		for row in self.__model:
			if size == row[1]: break
		iterator = self.__model.get_iter(row.path)
		self.__combo.set_active_iter(iterator)
		self.__combo.set_property("sensitive", True)
		return False

	def __update_cb(self, manager, configuration_data):
		self.__combo.handler_block(self.__sigid1)
		self.__set_active(configuration_data["size"])
		self.__combo.handler_unblock(self.__sigid1)
		return False

	def __changed_cb(self, *args):
		self.__combo.set_property("sensitive", False)
		iterator = self.__combo.get_active_iter()
		size = self.__model.get_value(iterator, 1)
		self.__manager.emit("new-configuration-data", ("size", size))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
