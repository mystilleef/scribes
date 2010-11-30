from gobject import GObject, SIGNAL_RUN_LAST, SIGNAL_NO_RECURSE
from gobject import SIGNAL_ACTION, TYPE_NONE, TYPE_PYOBJECT, TYPE_STRING
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"indent": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"unindent": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"marks": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"offsets": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"indentation": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"complete": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"extracted-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"processed-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"iprocessed-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"inserted-text": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"character": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Selector import Selector
		Selector(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from SelectionProcessor import Processor
		Processor(self, editor)
		from IndentationProcessor import Processor
		Processor(self, editor)
		from IndentationCharacter import Character
		Character(self, editor)
		from TextExtractor import Extractor
		Extractor(self, editor)
		from Marker import Marker
		Marker(self, editor)
		from OffsetExtractor import Extractor
		Extractor(self, editor)
		from Refresher import Refresher
		Refresher(self, editor)

	def indent(self):
		self.emit("indent")
		return

	def unindent(self):
		self.emit("unindent")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		return
