from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"check": (SSIGNAL, TYPE_NONE, ()),
		"errors-found": (SSIGNAL, TYPE_NONE, ()),
		"no-errors-found": (SSIGNAL, TYPE_NONE, ()),
		"no-error-message": (SSIGNAL, TYPE_NONE, ()),
		"check-tree": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"tree-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"syntax-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
