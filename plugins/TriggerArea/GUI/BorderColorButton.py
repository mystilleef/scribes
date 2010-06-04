from SCRIBES.SignalConnectionManager import SignalManager

class Button(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.connect(self.__button, "color-set", self.__color_cb)
		self.connect(manager, "configuration-data", self.__update_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__widget = manager.get_data("TriggerWidget")
		self.__button = manager.gui.get_object("BorderColorButton")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __set_active(self, color):
		from gtk.gdk import Color
		self.__button.set_color(Color(color))
		self.__button.set_property("sensitive", True)
		return False

	def __update_cb(self, manager, configuration_data):
		self.__button.handler_block(self.__sigid1)
		self.__set_active(configuration_data["border_color"])
		self.__button.handler_unblock(self.__sigid1)
		return False

	def __color_cb(self, *args):
		self.__button.set_property("sensitive", False)
		color = self.__button.get_color().to_string()
		self.__manager.emit("new-configuration-data", ("border_color", color))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
