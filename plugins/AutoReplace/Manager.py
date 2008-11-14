from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_STRING
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION, TYPE_PYOBJECT
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"match-found": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"no-match-found": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"dictionary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-update": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from BufferMonitor import Monitor
		Monitor(self, editor)
		from DictionaryManager import Manager
		Manager(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False

	def destroy(self):
		self.__destroy()
		return False
