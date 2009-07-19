from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_INT
from gobject import TYPE_STRING, TYPE_PYOBJECT, SIGNAL_RUN_FIRST
from gobject import TYPE_BOOLEAN, SIGNAL_ACTION, SIGNAL_NO_RECURSE
from gobject import SIGNAL_RUN_CLEANUP

SCRIBES_SIGNAL = SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-bar": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-replacebar": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-bar": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"search-string": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-pattern": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-regex": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-boundary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"search-complete": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"focus-entry": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"found-matches": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"marked-matches": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"mapped-matches": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-mode": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"popup-menu": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-menu": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"reset": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"next": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"previous": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"navigator-is-ready": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"current-match": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-mark": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"match-index": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"entry-activated": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"back-button": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"select-match": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"match-word-flag": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"match-case-flag": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-type-flag": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-mode-flag": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selection-bounds": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"replace": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"replace-all": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"replace-entry-activated": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"focus-replace-entry": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"replace-string": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"replaced-mark": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"regex-flags": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from MatchSelector import Selector
		Selector(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from BoundaryManager import Manager
		Manager(self, editor)
		from PatternCreator import Creator
		Creator(self, editor)
		from RegexCreator import Creator
		Creator(self, editor)
		from Searcher import Searcher
		Searcher(self, editor)
		from MatchMapper import Mapper
		Mapper(self, editor)
		from Marker import Marker
		Marker(self, editor)
		from MatchColorer import Colorer
		Colorer(self, editor)
		from MatchIndexer import Indexer
		Indexer(self, editor)
		from SelectionMatchColorer import Colorer
		Colorer(self, editor)
		from MatchNavigator import Navigator
		Navigator(self, editor)
		from ConfigurationManager import Manager
		Manager(self, editor)
		from ReplaceMatchColorer import Colorer
		Colorer(self, editor)
		from ReplaceManager import Manager
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

	def show_replacebar(self):
		self.emit("show-replacebar")
		self.emit("show-bar")
		return
