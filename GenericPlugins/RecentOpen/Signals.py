from SCRIBES.SIGNALS import GObject, TYPE_NONE, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"open-last-files": (SSIGNAL, TYPE_NONE, ()),
		"open-last-file": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
