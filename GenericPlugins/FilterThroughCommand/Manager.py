from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from CursorReseter import Reseter
		Reseter(self, editor)
		from ViewUpdater import Updater
		Updater(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from CommandExecutor import Executor
		Executor(self, editor)
		from BoundsExtractor import Extractor
		Extractor(self, editor)
		from NewWindowHandler import Handler
		Handler(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)
		from DatabaseReader import Reader
		Reader(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.glade"))
		return

	gui = property(lambda self: self.__gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
