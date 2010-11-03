from SCRIBES.SignalConnectionManager import SignalManager

scribes_dbus_service = "net.sourceforge.Scribes"
scribes_dbus_path = "/net/sourceforge/Scribes"

class Opener(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "open-files", self.__open_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __open(self, uris):
		from SCRIBES.Globals import session_bus
		proxy_object = session_bus.get_object(scribes_dbus_service, scribes_dbus_path)
		proxy_object.open_files(uris, dbus_interface=scribes_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		return False

	def __open_cb(self, manager, files):
		from gobject import idle_add
		idle_add(self.__open, files)
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, *args):
		print "ERROR: Failed to communicate with scribes process"
		return False
