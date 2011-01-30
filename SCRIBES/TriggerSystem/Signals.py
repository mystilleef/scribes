from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"add": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"quit": (SSIGNAL, TYPE_NONE, ()),
		"triggers-cleared": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
