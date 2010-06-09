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
		from GIOErrorHandler import Handler
		Handler(self)
		from Completer import Completer
		Completer(self)
		from FileReplacer import Replacer
		Replacer(self)
		from TextEncoder import Encoder
		Encoder(self)
		from JobSpooler import Spooler
		Spooler(self)
		self.emit("is-ready")
