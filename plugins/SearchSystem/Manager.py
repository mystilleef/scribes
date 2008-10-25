from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_INT
from gobject import TYPE_STRING, TYPE_PYOBJECT, SIGNAL_RUN_FIRST

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"search-string": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"new-pattern": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"new-regex": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-boundary": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search": (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
		"search-complete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"focus-entry": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"found-matches": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"marked-matches": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"mapped-matches": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-mode": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"popup-menu": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-menu": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"database-update": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"reset": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"next": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"previous": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"navigator-is-ready": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"current-match": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-mark": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"match-index": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"entry-activated": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"back-button": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"select-match": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from MatchSelector import Selector
		Selector(self, editor)
		from MatchMapper import Mapper
		Mapper(self, editor)
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
		from MatchIndexer import Indexer
		Indexer(self, editor)
		from MatchNavigator import Navigator
		Navigator(self, editor)
		from SelectionMatchColorer import Colorer
		Colorer(self, editor)
		from ConfigurationManager import Manager
		Manager(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		from os.path import join
		folder = editor.get_current_folder(globals())
		file_ = join(folder, "GUI/FindBar.glade")
		from gtk.glade import XML
		self.__glade = XML(file_, "BarWindow", "scribes")
		self.__mglade = XML(file_, "MenuWindow", "scribes")
		return

	gui = property(lambda self: self.__glade)
	menu_gui = property(lambda self: self.__mglade)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def show(self):
		self.emit("show-bar")
		return
