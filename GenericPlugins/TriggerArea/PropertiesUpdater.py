from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "configuration-data", self.__data_cb)
		self.connect(manager, "destroy", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__widget = manager.get_data("TriggerWidget")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, configuration_data):
		self.__editor.response()
		self.__widget.position = configuration_data["position"]
		self.__widget.size = configuration_data["size"]
		self.__widget.fill_color = configuration_data["fill_color"]
		self.__widget.border_color = configuration_data["fill_color"]
		self.__widget.queue_draw()
		self.__editor.textview.queue_draw()
		self.__editor.window.queue_draw()
		self.__editor.response()
		return False

	def __data_cb(self, manager, configuration_data):
		self.__update(configuration_data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
