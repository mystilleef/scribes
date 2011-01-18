from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from ProcessCommunicator import Communicator
		Communicator(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from MatchMonitor import Monitor
		Monitor(self, editor)
		from InsertedTextMonitor import Monitor
		Monitor(self, editor)
		from TriggerMarker import Marker 
		Marker(self, editor)
		from IndexerProcessManager import Manager
		Manager(self, editor)
		from IndexRequester import Requester
		Requester(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		self.__glade = editor.get_glade_object(globals(), join("GUI", "GUI.glade"), "Window")
		return

	gui = property(lambda self: self.__glade)

	def destroy(self):
		self.emit("destroy")
		del self
		return False
