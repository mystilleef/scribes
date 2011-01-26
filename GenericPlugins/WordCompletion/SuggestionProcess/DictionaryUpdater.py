from SCRIBES.Globals import session_bus
from SCRIBES.SignalConnectionManager import SignalManager

indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class Updater(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__manager = manager
		session_bus.add_signal_receiver(self.__finished_cb,
						signal_name="finished",
						dbus_interface=indexer_dbus_service)

	def __finished_cb(self, dictionary):
		self.__manager.emit("dictionary", dictionary)
		return False
