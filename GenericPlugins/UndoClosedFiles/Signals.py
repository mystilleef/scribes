from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"open-last-file": (SSIGNAL, TYPE_NONE, ()),
		"open-last-files": (SSIGNAL, TYPE_NONE, ()),
		"recent-infos": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"recent-uris": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
