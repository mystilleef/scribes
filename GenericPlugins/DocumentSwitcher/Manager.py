from gobject import SIGNAL_RUN_LAST, SIGNAL_NO_RECURSE, SIGNAL_ACTION
from gobject import TYPE_NONE, GObject
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"switch": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Switcher import Switcher
		Switcher(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return 

	def switch(self):
		self.emit("switch")
		return
