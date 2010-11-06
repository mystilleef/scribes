from dbus.service import Object, method, BusName, signal

indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class DBusService(Object):

	def __init__(self, manager):
		from SCRIBES.Globals import session_bus
		from dbus.exceptions import NameExistsException
		try:
			bus_name = BusName(indexer_dbus_service, bus=session_bus, do_not_queue=True)
			Object.__init__(self, bus_name, indexer_dbus_path)
			self.__manager = manager
			manager.connect("finished", self.__finished_cb)
		except NameExistsException:
			manager.quit()

	@method(indexer_dbus_service, in_signature="sx")
	def process(self, text, id_):
		return self.__manager.process(text, id_)

	@method(indexer_dbus_service)
	def index(self):
		return self.__manager.index()

	@signal(indexer_dbus_service, signature="a{sx}")
	def finished(self, dictionary):
		return

	def __finished_cb(self, manager, dictionary):
		self.finished(dictionary)
		return False
