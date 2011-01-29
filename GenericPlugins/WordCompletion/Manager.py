from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from ProcessCommunicator import Communicator
		Communicator(self, editor)
		from SuggestionProcessCommunicator import Communicator
		Communicator(self, editor)
		from TriggerMarker import Marker
		Marker(self, editor)
		from TriggerDetector import Detector
		Detector(self, editor)
		from IndexerProcessManager import Manager
		Manager(self, editor)
		from SuggestionProcessManager import Manager
		Manager(self, editor)
		from IndexRequester import Requester
		Requester(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)
		from DatabaseReader import Reader
		Reader(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)

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

	def activate(self):
		from Metadata import get_value
		enable_word_completion = not get_value()
		self.emit("update-database", enable_word_completion)
		# This looks very ugly. Fix later. Yeah right.
		from gettext import gettext as _
		ENABLE_MESSAGE = _("Enabled automatic word completion")
		DISABLE_MESSAGE = _("Disabled automatic word completion")
		feedback = self.__editor.update_message
		feedback(ENABLE_MESSAGE, "yes", 7) if enable_word_completion else feedback(DISABLE_MESSAGE, "no")
		return False
