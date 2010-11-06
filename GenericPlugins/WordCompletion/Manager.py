from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION, TYPE_STRING
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"inserting-text": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"inserted-text": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"dictionary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"match-found": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"no-match-found": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"valid-string": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"invalid-string": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"treeview-size": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"insert-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
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
		from IndexerProcessManager import Manager
		Manager(self, editor)

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
