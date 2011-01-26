from Signals import Signal

class Manager(Signal):

	def __init__(self):
		Signal.__init__(self)
		from ProcessMonitor import Monitor
		Monitor(self)
		from DBusService import DBusService
		DBusService(self)
		from SuggestionGenerator import Generator
		Generator(self)
		from DictionaryUpdater import Updater
		Updater(self)
		from gobject import timeout_add
		timeout_add(1000, self.__response)

	def generate(self, string):
		self.emit("string", string)
		return self.get_data("WordCompletionSuggestions")

	def quit(self):
		from os import _exit
		_exit(0)
		return False

	def __response(self):
		# Keep this process as responsive as possible to events and signals.
		from SCRIBES.Utils import response
		response()
		return True
