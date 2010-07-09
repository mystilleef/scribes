from SCRIBES.SignalConnectionManager import SignalManager

from PositionMetadata import set_value as position_value
from SizeMetadata import set_value as size_value
from FillColorMetadata import set_value as fill_value

UPDATE_DATABASE = {
	"position": position_value,
	"size": size_value,
	"fill_color": fill_value,
}

class Writer(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "new-configuration-data", self.__data_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, data):
		key, value = data
		UPDATE_DATABASE[key](value)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data)
		return False
