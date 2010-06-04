from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from TriggerWidget import TriggerWidget
		self.set_data("TriggerWidget", TriggerWidget())
		from TriggerHandler import Handler
		Handler(self, editor)
		from Positioner import Positioner
		Positioner(self, editor)
		from Displayer import Displayer
		Displayer(self, editor)
		from PropertiesUpdater import Updater
		Updater(self, editor)
		from FullViewHider import Hider
		Hider(self, editor)
		from FullViewActivator import Activator
		Activator(self, editor)
		from DatabaseReader import Reader
		Reader(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.glade"))
		return

	gui = property(lambda self: self.__gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def show(self):
		self.emit("show")
		return False

	def fullview(self):
		self.emit("fullview")
		return False
