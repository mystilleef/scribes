scribes_dbus_service = "net.sourceforge.Scribes"
scribes_dbus_path = "/net/sourceforge/Scribes"

def main():
	__fork_scribes()
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
	stdin = __get_pipe_input(args)
	from CommandLineProcessor import get_uris
	uris = get_uris(args, newfile) if stdin is None else ""
	__open_via_dbus(uris, stdin)
	from Utils import init_gnome
	init_gnome()
	from InstanceManager import Manager
	Manager().open_files(uris, "utf-8", stdin)
	return

def __get_pipe_input(args):
	if not ("-" in args): return None
	from sys import stdin
	_stdin = stdin.read()
	return _stdin

def __open_via_dbus(uris, stdin=""):
	dbus_service = __get_dbus_service()
	if not dbus_service: return
	uris = uris if uris else ""
	if stdin is None: stdin = ""
	dbus_service.open_files(uris, "utf-8", stdin, dbus_interface=scribes_dbus_service)
	raise SystemExit

def __get_dbus_service():
	from dbus.exceptions import DBusException
	try:
		from Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (scribes_dbus_service in services): return None
		proxy_object = session_bus.get_object(scribes_dbus_service, scribes_dbus_path)
	except DBusException:
		print "ERROR: Cannot find DBus session."
		raise SystemExit
	return proxy_object

def __fork_scribes():
	from ForkScribesMetadata import get_value as can_fork
	if not can_fork(): return
	from Utils import fork_process
	fork_process()
	return
