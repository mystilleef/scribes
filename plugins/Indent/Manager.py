from gobject import GObject, SIGNAL_RUN_LAST, SIGNAL_NO_RECURSE
from gobject import SIGNAL_ACTION, TYPE_NONE
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"indent": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"unindent": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)

	def indent(self):
		self.emit("indent")
		return

	def unindent(self):
		self.emit("unindent")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
