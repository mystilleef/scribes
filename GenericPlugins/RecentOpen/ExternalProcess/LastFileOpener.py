from SCRIBES.SignalConnectionManager import SignalManager

DBUS_SERVICE = "net.sourceforge.Scribes"
DBUS_PATH = "/net/sourceforge/Scribes"

class Opener(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(self.__manager, "recent-uris", self.__uris_cb)
		self.connect(self.__manager, "open-last-file", self.__file_cb)
		self.connect(self.__manager, "open-last-files", self.__files_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__uris = []
		self.__process = self.__get_process()
		return

	def __get_process(self):
		from SCRIBES.Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (DBUS_SERVICE in services): return None
		process = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
		return process

	def __open(self, number):
		count = 0
		uris = []
		open_uris = self.__process.get_uris(dbus_interface=DBUS_SERVICE)
		for uri in self.__uris:
			self.__manager.response()
			if uri in open_uris: continue
			count += 1
			uris.append(uri)
			if count == number: break
		if not uris: return False
		self.__manager.emit("open-files", uris)
		return False

	def __uris_cb(self, manager, uris):
		self.__uris = uris
		return False

	def __file_cb(self, *args):
		self.__open(1)
		return False

	def __files_cb(self, *args):
		self.__open(5)
		return False
