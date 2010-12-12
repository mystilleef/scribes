from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

data = ((_("Replace Content"), "replace"), (_("New Window"), "new"))

class ComboBox(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "output-mode", self.__output_cb)
		self.__sigid1 = self.connect(self.__combo, "changed", self.__changed_cb)
		self.__populate_model(data)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.gui.get_object("ComboBox")
		self.__model = self.__create_model()
		return False

	def __set_properties(self):
		from gtk import CellRendererText
		cell = CellRendererText()
		self.__combo.pack_end(cell, True)
		self.__combo.add_attribute(cell, "text", 0)
		self.__combo.set_model(self.__model)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_STRING
		model = ListStore(TYPE_STRING, TYPE_STRING)
		return model

	def __populate_model(self, data):
		self.__combo.handler_block(self.__sigid1)
		self.__combo.set_property("sensitive", False)
		self.__combo.set_model(None)
		self.__model.clear()
		for output, alias in data:
			self.__editor.refresh(False)
			self.__model.append([output, alias])
			self.__editor.refresh(False)
		self.__combo.set_model(self.__model)
		self.__combo.set_active(0)
		self.__combo.set_property("sensitive", True)
		self.__combo.handler_unblock(self.__sigid1)
		return False

	def __update_combo(self, output):
		self.__combo.handler_block(self.__sigid1)
		dictionary = {"replace": 0, "new": 1}
		self.__combo.set_active(dictionary[output])
		self.__combo.handler_unblock(self.__sigid1)
		return

	def __changed_cb(self, *args):
		iterator = self.__combo.get_active_iter()
		output = self.__model.get_value(iterator, 1)
		self.__manager.emit("update-database", output)
		return False

	def __output_cb(self, manager, output):
		self.__update_combo(output)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
