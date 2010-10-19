from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"to-unix": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"to-mac": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"to-windows": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Converter import Converter
		Converter(self, editor)

	def to_unix(self):
		self.emit("to-unix")
		return

	def to_mac(self):
		self.emit("to-mac")
		return

	def to_windows(self):
		self.emit("to-windows")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
