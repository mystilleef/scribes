from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_PYOBJECT, TYPE_NONE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"update": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"calculate": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from Displayer import Displayer
		Displayer(self, editor)
		from Tracker import Tracker
		Tracker(self, editor)
		from Timer import Timer
		Timer(self, editor)
		editor.response()
