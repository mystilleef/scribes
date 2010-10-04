from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_STRING
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION, TYPE_PYOBJECT
from gobject import TYPE_BOOLEAN
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"match-found": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"no-match-found": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"dictionary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update-dictionary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-update": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"edit-row": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"add-row": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"delete-row": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"sensitive": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"add-button-sensitivity": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"error": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from TextColorer import Colorer
		Colorer(self, editor)
		from BufferMonitor import Monitor
		Monitor(self, editor)
		from DictionaryManager import Manager
		Manager(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		self.__glade = editor.get_glade_object(globals(), join("GUI", "Window.glade"), "Window")
		return

	def __destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False

	gui = property(lambda self: self.__glade)

	def show(self):
		self.emit("show-window")
		return False

	def destroy(self):
		self.__destroy()
		return False
