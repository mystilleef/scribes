from SIGNALS import Signals

class Manager(Signals):

	def __init__(self):
		Signals.__init__(self)
		from DbusService import DbusService
		DbusService(self)
		from Quiter import Quiter
		Quiter()
		from ErrorManager import Manager
		Manager(self)
		from Completer import Completer
		Completer(self)
#		from FileTransferer import Transferer
#		Transferer(self)
#		from SwapFileWriter import Writer
#		Writer(self)
#		from SwapFileCreator import Creator
#		Creator(self)
		from FileReplacer import Replacer
		Replacer(self)
		from TextEncoder import Encoder
		Encoder(self)
#		from LocalURIPermissionChecker import Checker
#		Checker(self)
		from JobSpooler import Spooler
		Spooler(self)
		self.emit("is-ready")
