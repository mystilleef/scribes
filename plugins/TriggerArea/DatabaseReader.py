from SCRIBES.SignalConnectionManager import SignalManager

class Reader(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "database-update", self.__update_cb)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__update()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self):
		from PositionMetadata import get_value
		position = get_value()
		from SizeMetadata import get_value
		size = get_value()
		from BorderColorMetadata import get_value
		border_color = get_value()
		from FillColorMetadata import get_value
		fill_color = get_value()
		configuration_data = {
			"position": position,
			"size": size,
			"border_color": border_color,
			"fill_color": fill_color,
		}
		self.__manager.emit("configuration-data", configuration_data)
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
