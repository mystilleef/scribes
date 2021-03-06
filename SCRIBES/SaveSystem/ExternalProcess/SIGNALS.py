from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import TYPE_PYOBJECT, TYPE_INT
from gobject import SIGNAL_ACTION, SIGNAL_NO_RECURSE
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
		"gio-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"replace-file": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"encode-text": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		
	}

	def __init__(self):
		GObject.__init__(self)
