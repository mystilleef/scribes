def main():
	__start()
	from gobject import MainLoop, threads_init
	threads_init()
	MainLoop().run()
	return

def __start():
	if __save_process_exists(): raise SystemExit
	from gnome.ui import authentication_manager_init
	authentication_manager_init()
	from Manager import Manager
	Manager()
	return

def __save_process_exists():
	from SCRIBES.Globals import dbus_iface, SCRIBES_SAVE_PROCESS_DBUS_SERVICE
	services = dbus_iface.ListNames()
	if SCRIBES_SAVE_PROCESS_DBUS_SERVICE in services: return True
	return False
