from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"mapped": (SSIGNAL, TYPE_NONE, ()),
		"mark-selection": (SSIGNAL, TYPE_NONE, ()),
		"selection-marks": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"action": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"insertion-offsets": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"wrap-abbreviation": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
