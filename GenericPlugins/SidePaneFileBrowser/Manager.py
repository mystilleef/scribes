from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from os.path import join
		self.__gui = editor.get_gui_object(globals(), join("GUI", "GUI.ui"))
		from GUI.Manager import Manager
		Manager(self, editor)
		from FolderEnumerator import Enumerator
		Enumerator(self, editor)
		from FileinfosGenerator import Generator
		Generator(self, editor)
		from PathNavigator import Navigator
		Navigator(self, editor)
		from HistoryManager import Manager
		Manager(self, editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from FolderMonitor import Monitor
		Monitor(self, editor)
		from gobject import idle_add
		idle_add(self.emit, "generate-uris", editor.pwd_uri)

	@property
	def gui(self):
		return self.__gui

	def destroy(self):
		from gobject import idle_add
		idle_add(self.emit, "destroy")
		del self
		return False

	def activate(self):
		from gobject import idle_add
		idle_add(self.emit, "activate")
		return False
