class Monitor(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		from SCRIBES.Globals import SCRIBES_SAVE_PROCESS_DBUS_SERVICE, session_bus
		session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __save_process_exists(self):
		try:
			from dbus import DBusException
			from SCRIBES.Globals import dbus_iface, SCRIBES_SAVE_PROCESS_DBUS_SERVICE
			services = dbus_iface.ListNames()
			if not (SCRIBES_SAVE_PROCESS_DBUS_SERVICE in services): return False
		except DBusException:
			return False
		return True

	def __name_change_cb(self, *args):
		if self.__save_process_exists(): return
		self.__manager.emit("restart")
		return
