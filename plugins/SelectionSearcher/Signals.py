from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"reset": (SSIGNAL, TYPE_NONE, ()),
		"research": (SSIGNAL, TYPE_NONE, ()),
		"select-next-match": (SSIGNAL, TYPE_NONE, ()),
		"found-selection": (SSIGNAL, TYPE_NONE, ()),
		"select-previous-match": (SSIGNAL, TYPE_NONE, ()),
		"search-pattern": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"regex-object": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"found-matches": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"marked-matches": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"current-match": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
