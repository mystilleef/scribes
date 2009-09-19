from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_BOOLEAN
from gobject import TYPE_STRING, TYPE_OBJECT, TYPE_PYOBJECT, TYPE_INT
from gobject import SIGNAL_ACTION, type_register, SIGNAL_NO_RECURSE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION
SACTION = SIGNAL_RUN_LAST|SIGNAL_ACTION

class Signals(GObject):
	
	__gsignals__ = {
		# Nobody should listen to this signal. For internal use only.
		"close": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		# QUIT signal to all core objects. This signal is emitted only after
		# a file has been properly saved. For internal use only. PlEASE NEVER
		# EMIT THIS SIGNAL. This is the signal to listen to for proper cleanup
		# before exit.
		"quit": (SSIGNAL, TYPE_NONE, ()),
		"cursor-moved": (SSIGNAL, TYPE_NONE, ()),
		"ready": (SSIGNAL, TYPE_NONE, ()),
		"readonly": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"toggle-readonly": (SSIGNAL, TYPE_NONE, ()),
		"toggle-fullscreen": (SSIGNAL, TYPE_NONE, ()),
		"busy": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"private-busy": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"checking-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"loading-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"loaded-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"load-file": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT, TYPE_PYOBJECT)),
		"load-error": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"show-error": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_OBJECT, TYPE_BOOLEAN)),
		"show-info": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_OBJECT, TYPE_BOOLEAN)),
		"modified-file": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"enable-spell-checking": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"new-encoding-list": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update-encoding-guess-list": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"renamed-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"rename-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"reload-file": (SSIGNAL, TYPE_NONE, ()),
		"saved-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"save-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"private-save-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"save-error": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_STRING)),
		"send-data-to-processor": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING
		)),
		"private-encoding-load-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"dbus-saved-file": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"dbus-save-error": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_STRING)),
		"window-focus-out": (SSIGNAL, TYPE_NONE, ()),
		"combobox-encoding-data?": (SSIGNAL, TYPE_NONE, ()),
		"combobox-encoding-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"supported-encodings-window": (SSIGNAL, TYPE_NONE, (TYPE_OBJECT,)),
		"remove-bar-object": (SSIGNAL, TYPE_NONE, (TYPE_OBJECT,)),
		"add-bar-object": (SSIGNAL, TYPE_NONE, (TYPE_OBJECT,)),
		"spin-throbber": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"bar-is-active": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"update-message": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING, TYPE_INT,)),
		"set-message": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"unset-message": (SSIGNAL, TYPE_NONE, (TYPE_STRING, TYPE_STRING)),
		"undo": (SSIGNAL, TYPE_NONE, ()),
		"redo": (SSIGNAL, TYPE_NONE, ()),
		"add-trigger": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-trigger": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"add-triggers": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-triggers": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"register-object": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"unregister-object": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"trigger": (SSIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"refresh": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"add-to-popup": (SSIGNAL, TYPE_NONE, (TYPE_OBJECT,)),
		"add-to-pref-menu": (SSIGNAL, TYPE_NONE, (TYPE_OBJECT,)),
		"remove-from-pref-menu": (SSIGNAL, TYPE_NONE, (TYPE_OBJECT,)),
		"fullscreen": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
	}

	def __init__(self):
		GObject.__init__(self)
