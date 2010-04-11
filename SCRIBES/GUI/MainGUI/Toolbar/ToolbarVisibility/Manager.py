from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_BOOLEAN, TYPE_NONE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from Container import Container
		Container(self, editor)
		from MouseSensor import Sensor
		Sensor(self, editor)
		editor.response()
