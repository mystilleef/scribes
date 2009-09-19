from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE, TYPE_PYOBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"pattern": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"current-path": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"parent-path": (SSIGNAL, TYPE_NONE, ()),
		"get-fileinfos": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"folder-and-fileinfos": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"files": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"filtered-files": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"formatted-files": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"model-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-paths": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"uris": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"row-activated": (SSIGNAL, TYPE_NONE, ()),
		"updated-model": (SSIGNAL, TYPE_NONE, ()),
		"up-key-press": (SSIGNAL, TYPE_NONE, ()),
		"focus-entry": (SSIGNAL, TYPE_NONE, ()),
		"message": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"clear-message": (SSIGNAL, TYPE_NONE, ()),
		"entry-changed": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from URIOpener import Opener
		Opener(self, editor)
		from URIReconstructor import Reconstructor
		Reconstructor(self, editor)
		from MatchFilterer import Filterer
		Filterer(self, editor)
		from FileFormatter import Formatter
		Formatter(self, editor)
		from Enumerator import Enumerator
		Enumerator(self, editor)
		from FilesAggregator import Aggregator
		Aggregator(self, editor)
		from FolderPathUpdater import Updater
		Updater(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)

	def __init_attributes(self, editor):
		self.__gui = editor.get_gui_object(globals(), "GUI/GUI.glade")
		return

	gui = property(lambda self: self.__gui)

	def show(self):
		self.emit("show")
		return False

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False
