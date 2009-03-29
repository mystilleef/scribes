from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_BOOLEAN, TYPE_NONE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"database-query": (SSIGNAL, TYPE_NONE, ()),
		"minimal-mode": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from Container import Container
		Container(self, editor)
		from VisibilityManager import Manager
		Manager(self, editor)
		from FullscreenManager import Manager
		Manager(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		editor.response()
