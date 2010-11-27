from SCRIBES.SIGNALS import GObject, TYPE_NONE, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"next-window": (SSIGNAL, TYPE_NONE, ()),
		"previous-window": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
