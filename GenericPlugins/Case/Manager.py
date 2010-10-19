from gobject import SIGNAL_RUN_LAST, SIGNAL_NO_RECURSE, SIGNAL_ACTION
from gobject import TYPE_PYOBJECT, TYPE_NONE, TYPE_STRING, GObject
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"marks": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"extracted-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"processed-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"text-inserted": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"complete": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"case": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Selector import Selector
		Selector(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from CaseProcessor import Processor
		Processor(self, editor)
		from TextExtractor import Extractor
		Extractor(self, editor)
		from Marker import Marker
		Marker(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False

	def toggle(self):
		self.emit("case", "toggle")
		return False

	def title(self):
		self.emit("case", "title")
		return False

	def swap(self):
		self.emit("case", "swap")
		return False
