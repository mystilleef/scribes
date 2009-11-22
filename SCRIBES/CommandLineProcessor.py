__OPTIONS = (
			"-v", "-version", "--version",
			"-n", "-newfile", "--newfile",
			"-i", "-info", "--info",
			"-h", "-help", "--help")

__help_message = "Try 'scribes --help' for more information"
__error_message1 = "ERROR: Use only one option at a time."
__error_message2 = "Unrecognized option: '%s'"

def get_uris(argv):
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
	from gio import File
	uris = [File(arg).get_uri() for arg in arguments]
	fake_uris = [uri for uri in uris if not __exists(uri)]
	__create_files(fake_uris) if fake_uris and create_flag else __print_no_exist(fake_uris)
	uris = [uri for uri in uris if __exists(uri)]
	return uris

def __exists(uri):
	# Do not perform checks on remote files.
	from gio import File
	if File(uri).get_uri_scheme() != "file": return True
	from os.path import exists
	return exists(File(uri).get_path())

def __print_info():
	from CommandLineInfo import print_info
	print_info()
	return

def __print_help():
	from Usage import help as chelp
	chelp()
	return

def __print_version():
	from Globals import version
	from i18n import msg0042
	from locale import getpreferredencoding
	encoding = getpreferredencoding(True)
	print msg0042.decode("utf-8").encode(encoding) % \
	version.encode(encoding, "replace")
	return

def __print_no_exist(uris):
	if not uris: return False
	from gio import File
	for uri in uris: print File(uri).get_path(), " does not exists"
	return False

def __create(uri):
	try:
		from gio import File
		if File(uri).get_uri_scheme() != "file": raise ValueError
		File(uri).replace_contents("")
	except ValueError:
		print "Error: %s is a remote file. Cannot create remote files from \
		terminal" % File(uri).get_path()
	except:
		print "Error: could not create %s" % File(uri).get_path()
	return False

def __create_files(uris):
	for uri in uris: __create(uri)
	return False

def __quit_message(message):
	print message
	print __help_message
	raise SystemExit
	return False
