from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_BOOLEAN
from gobject import TYPE_STRING, TYPE_PYOBJECT, TYPE_INT
from gobject import SIGNAL_ACTION, type_register, SIGNAL_NO_RECURSE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Signals(GObject):

	__gsignals__ = {
		"save-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"check-permission": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update-id": (SSIGNAL, TYPE_NONE, (TYPE_INT,)),
		"is-ready": (SSIGNAL, TYPE_NONE, ()),
		"saved-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"oops": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"create-swap-file": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"write-to-swap-file": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"encode-text": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"transfer": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
