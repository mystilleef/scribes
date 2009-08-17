from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE, TYPE_PYOBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		print "manager initialized"
		editor.response()
