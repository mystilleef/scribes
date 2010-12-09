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
		from gobject import timeout_add
		timeout_add(1000, self.__response)
		self.emit("is-ready")

	def __response(self):
		# Make this process as responsive as possible to signals and events.
		from SCRIBES.Utils import response
		response()
		return True
