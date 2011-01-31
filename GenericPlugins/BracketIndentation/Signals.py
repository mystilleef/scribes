from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"done": (SSIGNAL, TYPE_NONE, ()),
		"empty-brackets": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"mark-bracket-region": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"insert": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
