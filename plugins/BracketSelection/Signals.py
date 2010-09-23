from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"no-pair-character-found": (SSIGNAL, TYPE_NONE, ()),
		"find-open-character": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"found-open-character": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"check-pair-range": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"select-offsets": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
