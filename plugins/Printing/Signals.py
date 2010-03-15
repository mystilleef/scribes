from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"cancel": (SSIGNAL, TYPE_NONE, ()),
		"feedback": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
