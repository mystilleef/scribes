from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_OBJECT, TYPE_STRING
from gobject import TYPE_NONE, TYPE_INT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"init-loading": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"check-local-uri": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"check-remote-uri": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"read-uri": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"error": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_INT)),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor, uri, encoding):
		GObject.__init__(self)
		from StateNotifier import Notifier
		Notifier(self, editor)
		from ErrorManager import Manager
		Manager(self, editor)
		from RemoteURIPermissionChecker import Checker
		Checker(self, editor)
		from LocalURIPermissionChecker import Checker
		Checker(self, editor)
		from URITypeChecker import Checker
		Checker(self, editor)
		from Initializer import Initializer
		Initializer(self, editor, uri, encoding)
		
