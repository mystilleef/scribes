from dbus.service import Object, method, BusName

from Utils import DBUS_SERVICE, DBUS_PATH

class DBusService(Object):

	def __init__(self, manager):
		from SCRIBES.Globals import session_bus
		from dbus.exceptions import NameExistsException
		try:
			bus_name = BusName(DBUS_SERVICE, bus=session_bus, do_not_queue=True)
			Object.__init__(self, bus_name, DBUS_PATH)
			self.__manager = manager
		except NameExistsException:
			manager.quit()

	@method(DBUS_SERVICE)
	def activate(self):
		return self.__manager.activate()

	@method(DBUS_SERVICE)
	def open_last_file(self):
		return self.__manager.open_last_file()

	@method(DBUS_SERVICE)
	def open_last_files(self):
		return self.__manager.open_last_files()
