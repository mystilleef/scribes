from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"_hide": (SSIGNAL, TYPE_NONE, ()),
		"_show": (SSIGNAL, TYPE_NONE, ()),
		"bar": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"bar-size": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"view-size": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"deltas": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"animation": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"slide": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"visible": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
