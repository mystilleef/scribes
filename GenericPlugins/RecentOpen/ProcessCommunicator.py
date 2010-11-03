from ExternalProcess.Utils import DBUS_SERVICE, DBUS_PATH
from SCRIBES.SignalConnectionManager import SignalManager

class Communicator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "open-last-file", self.__file_cb)
		self.connect(manager, "open-last-files", self.__files_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=DBUS_SERVICE)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__process = self.__get_process()
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=DBUS_SERVICE)
		del self
		return False

	def __get_process(self):
		from SCRIBES.Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (DBUS_SERVICE in services): return None
		process = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
		return process

	def __activate(self, process_method):
		try:
			process_method(dbus_interface=DBUS_SERVICE,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except AttributeError:
			pass
		except Exception:
			print "ERROR: Cannot send message to python checker process"
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate, self.__process.activate)
		return False

	def __file_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate, self.__process.open_last_file)
		return False

	def __files_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate, self.__process.open_last_files)
		return False

	def __name_change_cb(self, *args):
		self.__process = self.__get_process()
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, *args):
		print "ERROR: Failed to communicate with scribes python checker process"
		return False
