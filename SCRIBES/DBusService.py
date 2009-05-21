from dbus.service import Object, method, BusName

class DBusService(Object):

	def __init__(self, manager):
		from Globals import session_bus
		service_name = "net.sourceforge.Scribes"
		object_path = "/net/sourceforge/Scribes"
		bus_name = BusName(service_name, bus=session_bus)
		Object.__init__(self, bus_name, object_path)
		self.__manager = manager

	@method("net.sourceforge.Scribes")
	def open_window(self):
		return self.__manager.open_window()

	@method("net.sourceforge.Scribes", in_signature="as")
	def open_files(self, uris):
		uris = uris if uris else None
		return self.__manager.open_files(uris)
