from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE
from gobject import TYPE_PYOBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"slide": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"animation": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"deltas": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"size": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"visible": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from HideTimer import Timer
		Timer(self, editor)
		from APIVisibilityUpdater import Updater
		Updater(self, editor)
		from VisibilityUpdater import Updater
		Updater(self, editor)
		from Resizer import Resizer
		Resizer(self, editor)
		from Animator import Animator
		Animator(self, editor)
		from Displayer import Displayer
		Displayer(self, editor)
		from MouseSensor import Sensor
		Sensor(self, editor)
		from DeltaCalculator import Calculator
		Calculator(self, editor)
		from SizeUpdater import Updater
		Updater(self, editor)
