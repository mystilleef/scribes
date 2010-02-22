class Parser(object):

	def __init__(self):
		self.__init_attributes()
		self.__add_options()
		self.__args = self.__parser.parse_args()[-1]

	def __init_attributes(self):
		from optparse import OptionParser
		self.__parser = OptionParser()
		self.__args = []
		self.__readonly = False
		self.__encoding = "utf-8"
		self.__newfile = False
		return

	args = property(lambda self: self.__args)
	readonly = property(lambda self: self.__readonly)
	encoding = property(lambda self: self.__encoding)
	newfile = property(lambda self: self.__newfile)

	def __add_options(self):
		parser = self.__parser
		parser.add_option("-v", "--version",
			help="display the version of Scribes currently running",
			action="callback",
			callback=self.__print_version)
		parser.add_option("-i", "--info",
			help="display detailed information about Scribes",
			action="callback",
			callback=self.__print_info)
		parser.add_option("-n", "--newfile",
			help="create a new file and open the file in Scribes",
			action="callback",
			callback=self.__enable_newfile)
		parser.add_option("-e", "--encoding",
			help="open file(s) with specified encoding",
			action="callback",
			callback=self.__update_encoding)
		parser.add_option("-r", "--readonly",
			help="open file(s) in readonly mode",
			action="callback",
			callback=self.__enable_readonly)
		return

	def __print_version(self, *args):
		from Globals import version
		from i18n import msg0042
		from locale import getpreferredencoding
		encoding = getpreferredencoding(True)
		print msg0042.decode("utf-8").encode(encoding) % version.encode(encoding, "replace")
		raise SystemExit
		return False

	def __print_info(self, *args):
		from CommandLineInfo import print_info
		print_info()
		raise SystemExit
		return False

	def __enable_newfile(self, *args):
		self.__newfile = True
		return False

	def __update_encoding(self, *args):
		self.__encoding = "utf-8"
		return False

	def __enable_readonly(self, *args):
		self.__readonly = True
		return False
