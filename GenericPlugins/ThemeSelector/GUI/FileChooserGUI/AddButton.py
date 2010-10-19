from SCRIBES.SignalConnectionManager import SignalManager

class Button(SignalManager):

	def __init__(self, editor, manager):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "valid-chooser-selection", self.__valid_cb)
		self.connect(self.__button, "clicked", self.__clicked_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.chooser_gui.get_object("AddButton")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __valid_cb(self, manager, value):
		self.__button.set_property("sensitive", value)
		return

	def __clicked_cb(self, *args):
		self.__manager.emit("activate-chooser")
		return
