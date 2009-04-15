dbus_service = "org.sourceforge.ScribesSaveProcessor"
dbus_path = "/org/sourceforge/ScribesSaveProcessor"

class SaveProcessor(object):

	def __init__(self):
		self.__start_up_check()
		from SaveProcessorDBusService import DBusService
		dbus = DBusService(self)
		self.__init_attributes(dbus)
		from Globals import session_bus as session
		session.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0='net.sourceforge.Scribes')
		dbus.is_ready()

	def __init_attributes(self, dbus):
		from OutputProcessor import OutputProcessor
		self.__processor = OutputProcessor(dbus)
		return

	def save_file(self, session_id, text, uri, encoding):
		from thread import start_new_thread
		start_new_thread(self.__save_file, (session_id, text, uri, encoding))
		return

	def update(self, editor_id):
		from thread import start_new_thread
		start_new_thread(self.__update, (editor_id,))
		return

	def __save_file(self, session_id, text, uri, encoding):
		from thread import start_new_thread
		start_new_thread(self.__processor.process, (session_id, text, uri, encoding))
		return False

	def __update(self, editor_id):
		from thread import start_new_thread
		start_new_thread(self.__processor.update, (editor_id,))
		return False

	def __name_change_cb(self, *args):
		from os import _exit
		_exit(0)
		return

	def __start_up_check(self):
		from Globals import dbus_iface
		services = dbus_iface.ListNames()
		if not (dbus_service in services): return
		from os import _exit
		_exit(0)
		return

def __init_psyco():
	try:
		from psyco import full
		full()
	except ImportError:
		pass
	return False

if __name__ == "__main__":
	from sys import argv, path
	python_path = argv[1]
	path.insert(0, python_path)
	from gnome.ui import authentication_manager_init
	authentication_manager_init()
	SaveProcessor()
	__init_psyco()
	from gobject import MainLoop, threads_init
	threads_init()
	MainLoop().run()
