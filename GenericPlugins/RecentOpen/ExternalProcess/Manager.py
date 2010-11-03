from Signals import Signal

class Manager(Signal):

	def __init__(self):
		Signal.__init__(self)
		self.__init_attributes()
		from ProcessMonitor import Monitor
		Monitor(self)
		from DBusService import DBusService
		DBusService(self)
		from GUI.Manager import Manager
		Manager(self)
		from LastFileOpener import Opener
		Opener(self)
		from Feedback import Feedback
		Feedback(self)
		from MatchFilterer import Filterer
		Filterer(self)
		from DataGenerator import Generator
		Generator(self)
		from FileOpener import Opener
		Opener(self)
		from RecentInfoListener import Listener
		Listener(self)
		from gobject import timeout_add
		timeout_add(1000, self.__response)

	def __init_attributes(self):
		from os.path import join
		from SCRIBES.Utils import get_gui_object
		self.__gui = get_gui_object(globals(), join("GUI", "GUI.glade"))
		return

	@property
	def gui(self): return self.__gui

	def quit(self):
		from os import _exit
		_exit(0)
		return False

	def activate(self):
		self.emit("activate")
		return False

	def open_last_file(self):
		self.emit("open-last-file")
		return False

	def open_last_files(self):
		self.emit("open-last-files")
		return False

	def __response(self):
		# Keep this process as responsive as possible to events and signals.
		from SCRIBES.Utils import response
		response()
		return True

	def response(self):
		from SCRIBES.Utils import response
		response()
		return False
