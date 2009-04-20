class Quiter(object):

	def __init__(self):
		from SCRIBES.Globals import session_bus as session
		from SCRIBES.Globals import SCRIBES_DBUS_SERVICE
		session.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=SCRIBES_DBUS_SERVICE)

	def __scribes_process_exists(self):
		from SCRIBES.Globals import dbus_iface, SCRIBES_DBUS_SERVICE
		services = dbus_iface.ListNames()
		if SCRIBES_DBUS_SERVICE in services: return True
		return False

	def __quit(self):
		if self.__scribes_process_exists(): return False
		from os import _exit
		_exit(0)
		return False

	def __name_change_cb(self, *args):
		self.__quit()
		return False
