__OPTIONS = ("-v", "-version", "--version",
			"-n", "-newfile", "--newfile",
			"-i", "-info", "--info",
			"-h", "-help", "--help")

__help_message = "Try 'scribes --help' for more information"
__error_message1 = "ERROR: Use only one option at a time."
__error_message2 = "Unrecognized option: '%s'"

def get_uris(argv):
	uris = []
	options = [option for option in argv if option.startswith("-")]
	arguments = [argument.strip() for argument in argv if not argument.startswith("-")]
	__process_options(options)
	option = options[0] if options else None
	uris = __uris_from_arguments(arguments, option)
	return uris

def __process_options(options):
	if not options: return False
	if len(options) > 1: __quit_message(__error_message1)
	option = options[0]
	if not (option in __OPTIONS): __quit_message(__error_message2 % option)
	if option in ("-n", "-newfile", "--newfile"): return False
	if option in ("-v", "-version", "--version"): __print_version()
	if option in ("-h", "-help", "--help"): __print_help()
	if option in ("-i", "-info", "--info"): __print_info()
	raise SystemExit
	return False

def __uris_from_arguments(arguments, option):
	create_flag = True if option in ("-n", "-newfile", "--newfile") else False
	if create_flag and not arguments: __quit_message(option + " takes one or more arguments")
	from gnomevfs import make_uri_from_shell_arg, exists
	uris = [make_uri_from_shell_arg(arg) for arg in arguments]
	fake_uris = [uri for uri in uris if not exists(uri)]
	__create_files(fake_uris) if fake_uris and create_flag else __print_no_exist(fake_uris)
	uris = [uri for uri in uris if exists(uri)]
	return uris

def __print_info():
	from CommandLineInfo import print_info
	print_info()
	return

def __print_help():
	from usage import help as chelp
	chelp()
	return

def __print_version():
	from info import version
	from internationalization import msg0042
	from locale import getpreferredencoding
	encoding = getpreferredencoding(True)
	print msg0042.decode("utf-8").encode(encoding) % \
	version.encode(encoding, "replace")
	return

def __print_no_exist(uris):
	if not uris: return False
	from gnomevfs import get_local_path_from_uri
	for uri in uris: print get_local_path_from_uri(uri), " does not exists"
	return False

def __create(uri):
	try:
		if not uri.startswith("file:///"): raise ValueError
		from gnomevfs import create, OPEN_WRITE
		create(uri, OPEN_WRITE)
	except ValueError:
		from gnomevfs import get_local_path_from_uri
		print "Error: %s is a remote file. Cannot create remote files from \
		terminal" % get_local_path_from_uri(uri)
	except:
		from gnomevfs import get_local_path_from_uri
		print "Error: could not create %s" % get_local_path_from_uri(uri)
	return False

def __create_files(uris):
	for uri in uris: __create(uri)
	return False

def __quit_message(message):
	print message
	print __help_message
	raise SystemExit
	return False
