from gobject import GObject, TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gobject import SIGNAL_RUN_LAST, SIGNAL_ACTION, SIGNAL_NO_RECURSE
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy":(SCRIBES_SIGNAL, TYPE_NONE, ()),
		"processed-text":(SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"extracted-text":(SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"spaces-to-tabs":(SCRIBES_SIGNAL, TYPE_NONE, ()),
		"tabs-to-spaces":(SCRIBES_SIGNAL, TYPE_NONE, ()),
		"remove-trailing-spaces":(SCRIBES_SIGNAL, TYPE_NONE, ()),
		"inserted-text":(SCRIBES_SIGNAL, TYPE_NONE, ()),
		"position":(SCRIBES_SIGNAL, TYPE_NONE, ()),
		"line-offset":(SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from CursorPositioner import Positioner
		Positioner(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from SpaceProcessor import Processor
		Processor(self, editor)
		from TextExtractor import Extractor
		Extractor(self, editor)
		from OffsetGetter import Getter
		Getter(self, editor)
		editor.response()

	def spaces_to_tabs(self):
		self.emit("position")
		self.emit("spaces-to-tabs")
		return False

	def tabs_to_spaces(self):
		self.emit("position")
		self.emit("tabs-to-spaces")
		return False

	def remove_trailing_spaces(self):
		self.emit("position")
		self.emit("remove-trailing-spaces")
		return False

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False
