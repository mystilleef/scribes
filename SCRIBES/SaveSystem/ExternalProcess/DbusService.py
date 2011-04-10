from dbus.service import Object, method, BusName, signal
from SCRIBES.Globals import SCRIBES_SAVE_PROCESS_DBUS_SERVICE as dbus_service

class DbusService(Object):

	def __init__(self, manager):
		from SCRIBES.Globals import session_bus as session
		from SCRIBES.Globals import SCRIBES_SAVE_PROCESS_DBUS_PATH
		bus_name = BusName(dbus_service, bus=session)
		Object.__init__(self, bus_name, SCRIBES_SAVE_PROCESS_DBUS_PATH)
		self.__manager = manager
		manager.connect("is-ready", self.__is_ready_cb)
		manager.connect("saved-data", self.__saved_data_cb)
		manager.connect("error", self.__error_cb)

	@method(dbus_service, in_signature="(atsss)")
	def process(self, data):
		from gobject import idle_add
		return idle_add(self.__manager.emit, "save-data", data)

	@signal(dbus_service)
	def is_ready(self):
		return False

	@signal(dbus_service, signature="(axss)")
	def saved_file(self, data):
		return False

	@signal(dbus_service)
	def error(self, data):
		return False

	def __is_ready_cb(self, *args):
		from gobject import idle_add
		idle_add(self.is_ready)
		return False

	def __saved_data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.saved_file, data)
		return False

	def __error_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.error, data)
		return False
