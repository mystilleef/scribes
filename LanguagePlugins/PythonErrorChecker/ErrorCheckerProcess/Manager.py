from Signals import Signal
SETCHECKINTERVAL = 10000

class Manager(Signal):

	def __init__(self):
		Signal.__init__(self)
		from sys import setcheckinterval
		setcheckinterval(SETCHECKINTERVAL)
		from ProcessMonitor import Monitor
		Monitor(self)
		from DBusService import DBusService
		DBusService(self)
		from PyChecker import Checker
		Checker(self)
		from PyLintChecker import Checker
		Checker(self)
		from PyFlakesChecker import Checker
		Checker(self)
		from SyntaxChecker import Checker
		Checker(self)
		from JobSpooler import Spooler
		Spooler(self)
		from gobject import timeout_add
		timeout_add(1000, self.__response)

	def quit(self): 
		from os import _exit
		_exit(0)
		return False

	def check(self, data):
		self.emit("new-job", data)
		return False

	def stop(self, data):
		self.emit("stop", data)
		return False

	def __response(self):
		# Keep this process as responsive as possible to events and signals.
		from SCRIBES.Utils import response
		response()
		return True
