from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_INT
from gobject import TYPE_STRING, TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"search-string": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"new-pattern": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"new-regex": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-boundary": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"focus-entry": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"found-matches": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"marked-matches": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from MatchColorer import Colorer
		Colorer(self, editor)
		from Marker import Marker
		Marker(self, editor)
		from BoundaryManager import Manager
		Manager(self, editor)
		from Searcher import Searcher
		Searcher(self, editor)
		from PatternCreator import Creator
		Creator(self, editor)
		from RegexCreator import Creator
		Creator(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		from os.path import join
		folder = editor.get_current_folder(globals())
		file_ = join(folder, "GUI/FindBar.glade")
		from gtk.glade import XML
		self.__glade = XML(file_, "Window", "scribes")
		return

	gui = property(lambda self: self.__glade)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def show(self):
		self.emit("show-bar")
		return
