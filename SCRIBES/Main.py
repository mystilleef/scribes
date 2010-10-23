scribes_dbus_service = "net.sourceforge.Scribes"
scribes_dbus_path = "/net/sourceforge/Scribes"

def main():
	from gobject import threads_init
	threads_init()
	__open()
	from gtk import main
	main()
	return

def __open():
	from CommandLineParser import Parser
	parser = Parser()
	args, newfile = parser.args, parser.newfile
	from CommandLineProcessor import get_uris
	uris = get_uris(args, newfile)
	__open_via_dbus(uris)
	from Utils import init_gnome
	init_gnome()
	from InstanceManager import Manager
	Manager().open_files(uris)
	return

def __open_via_dbus(uris):
	dbus_service = __get_dbus_service()
	if not dbus_service: return
	uris = uris if uris else ""
	dbus_service.open_files(uris, dbus_interface=scribes_dbus_service)
	raise SystemExit
	return

def __get_dbus_service():
	from Globals import dbus_iface, session_bus
	services = dbus_iface.ListNames()
	if not (scribes_dbus_service in services): return None
	proxy_object = session_bus.get_object(scribes_dbus_service, scribes_dbus_path)
	return proxy_object

def __fork_scribes():
	# Very buggy. Don't use for now.
	from ForkScribesMetadata import get_value as can_fork
	if not can_fork(): return
	from os import fork
	pid = fork()
	if pid != 0: raise SystemExit
	return
