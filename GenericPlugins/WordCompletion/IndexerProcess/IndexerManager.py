from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION
from gtk import main_iteration, events_pending
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"get-text": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"new-job": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"no-change": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"index-request": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"index": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"content": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"clipboard-text": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
		from IndexerProcessMonitor import Monitor
		Monitor(self)
		from DBusService import DBusService
		DBusService(self)
		from DictionaryGenerator import Generator
		Generator(self)
		from DiffManager import Manager
		Manager(self)
		from TextGetter import Getter
		Getter(self)
		from ClipboardManager import Manager
		Manager(self)
		from JobSpooler import Spooler
		Spooler(self)
		# Keep this process as responsive as possible to events and signals.
		from gobject import timeout_add
		timeout_add(1000, self.response)
		from os import nice
		nice(19)

	def quit(self):
		from os import _exit
		_exit(0)
		return

	def index(self):
		self.emit("index-request")
		return False

	def response(self):
		while events_pending(): main_iteration(False)
		return True
