from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from ViewUpdater import Updater
		Updater(self, editor)
		from UndoRedoManager import Manager
		Manager(self, editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from PlaceholderColorer import Colorer
		Colorer(self, editor)
		from PlaceholderCursorMonitor import Monitor
		Monitor(self, editor)
		from TextInsertionMonitor import Monitor
		Monitor(self, editor)
		from BoundaryCursorMonitor import Monitor
		Monitor(self, editor)
		from PlaceholderNavigator import Navigator
		Navigator(self, editor)
		from KeyboardHandler import Handler
		Handler(self, editor)
		from PlaceholderRemover import Remover
		Remover(self, editor)
		from PlaceholderSearcher import Searcher
		Searcher(self, editor)
		from MarkManager import Manager
		Manager(self, editor)
		from TemplateInserter import Inserter
		Inserter(self, editor)
		from AbbreviationExpander import Expander
		Expander(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)

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
