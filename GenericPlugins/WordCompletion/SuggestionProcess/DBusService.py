from dbus.service import Object, method, BusName

DBUS_SERVICE = "org.sourceforge.ScribesWordCompletionSuggestionGenerator"
DBUS_PATH = "/org/sourceforge/ScribesWordCompletionSuggestionGenerator"

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

	@method(DBUS_SERVICE, in_signature="s", out_signature="as")
	def generate(self, string):
		return self.__manager.generate(string)
