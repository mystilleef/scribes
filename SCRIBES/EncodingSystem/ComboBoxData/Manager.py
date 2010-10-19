from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE, TYPE_PYOBJECT
from gobject import TYPE_OBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"database-changed": (SSIGNAL, TYPE_NONE, ()),
		"encoding-list": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Generator import Generator
		Generator(self, editor)
		from ..SupportedEncodings.EncodingListDispatcher import Dispatcher
		Dispatcher(self, editor)
		from ..SupportedEncodings.EncodingListDatabaseMonitor import Monitor
		Monitor(self, editor)
