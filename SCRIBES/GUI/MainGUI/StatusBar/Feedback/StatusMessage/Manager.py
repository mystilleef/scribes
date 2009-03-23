from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_OBJECT, TYPE_STRING
from gobject import TYPE_NONE, TYPE_INT, TYPE_BOOLEAN
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"set-message": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"update-message": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_BOOLEAN, TYPE_BOOLEAN, TYPE_STRING)),
		"update": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_INT)),
		"set": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"unset": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"busy": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"reset": (SSIGNAL, TYPE_NONE, ()),
		"fallback": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		editor.response()
		from MessageDisplayer import Displayer
		Displayer(self, editor)
		from FeedbackDispatcher import Dispatcher
		Dispatcher(self, editor)
		from MessageFormatter import Formatter
		Formatter(self, editor)
		from StackMessageSwitcher import Switcher
		Switcher(self, editor)
		from FallbackMessageSwitcher import Switcher
		Switcher(self, editor)
		from FileModificationStateSwitcher import Switcher
		Switcher(self, editor)
		from SavedStateSwitcher import Switcher
		Switcher(self, editor)
		from TimedMessageSwitcher import Switcher
		Switcher(self, editor)
		from FileLoadingStateSwitcher import Switcher
		Switcher(self, editor)
		editor.response()
