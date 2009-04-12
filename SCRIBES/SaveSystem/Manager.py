from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_PYOBJECT
from gobject import TYPE_NONE, TYPE_PYOBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"session-id": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"validate-save-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-processor-object": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"readonly-error": (SSIGNAL, TYPE_NONE, ()),
		"show-save-dialog": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from SessionManager import Manager
		Manager(self, editor)
		from DataValidator import Validator
		Validator(self, editor)
		from ReadonlyHandler import Handler
		Handler(self, editor)
		from SaveDialogDisplayer import Displayer
		Displayer(self, editor)
		from DbusDataSender import Sender
		Sender(self, editor)
		from DbusSaveProcessorMonitor import Monitor
		Monitor(self, editor)
		editor.response()
