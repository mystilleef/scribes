from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_PYOBJECT
from gobject import TYPE_NONE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"session-id": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-processor-object": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-succeeded": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"saved": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"saved?": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"save-failed": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"readonly-error": (SSIGNAL, TYPE_NONE, ()),
		"reset-modification-flag": (SSIGNAL, TYPE_NONE, ()),
		"generate-name": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"newname": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"create-new-file": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"created-new-file": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-save-job": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"start-save-job": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished-save-job": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"saving-in-progress": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-new-file": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from AutomaticSaver import Saver
		Saver(self, editor)
		from FocusOutSaver import Saver
		Saver(self, editor)
		from UnnamedDocumentCreator import Creator
		Creator(self, editor)
		from QuitSaver import Saver
		Saver(self, editor)
		from NewFileRemover import Remover
		Remover(self, editor)
		from FileModificationMonitor import Monitor
		Monitor(self, editor)
		from SessionCompleter import Completer
		Completer(self, editor)
		from FileNameGenerator import Generator
		Generator(self, editor)
		from NameGenerator import Generator
		Generator(self, editor)
		from SessionManager import Manager
		Manager(self, editor)
		from ReadonlyHandler import Handler
		Handler(self, editor)
		from ErrorDisplayer import Displayer
		Displayer(self, editor)
		from SaveErrorSignalEmitter import Emitter
		Emitter(self, editor)
		from SavedSignalEmitter import Emitter
		Emitter(self, editor)
		from DbusDataReceiver import Receiver
		Receiver(self, editor)
		from DbusDataSender import Sender
		Sender(self, editor)
		from DbusSaveProcessorMonitor import Monitor
		Monitor(self, editor)
		from SaveJobMonitor import Monitor
		Monitor(self, editor)
		from SaveJobSpooler import Spooler
		Spooler(self, editor)

