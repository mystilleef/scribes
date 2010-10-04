from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"fullview": (SSIGNAL, TYPE_NONE, ()),
		"database-update": (SSIGNAL, TYPE_NONE, ()),
		"configuration-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-configuration-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
