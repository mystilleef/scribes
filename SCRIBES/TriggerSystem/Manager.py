from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE, TYPE_PYOBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"add": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"quit": (SSIGNAL, TYPE_NONE, ()),
		"triggers-cleared": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Bindings.Manager import Manager
		Manager(editor)
		from Quiter import Quiter
		Quiter(self, editor)
		from TriggerManager import Manager
		Manager(self, editor)
		from TriggerActivator import Activator
		Activator(self, editor)
		from AcceleratorActivator import Activator
		Activator(self, editor)
		from TriggerRemover import Remover
		Remover(self, editor)
		from Validator import Validator
		Validator(self, editor)
