from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"mapped": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"failed": (SSIGNAL, TYPE_NONE, ()),
		"finish": (SSIGNAL, TYPE_NONE, ()),
		"remove-marks": (SSIGNAL, TYPE_NONE, ()),
		"removed-placeholders": (SSIGNAL, TYPE_NONE, ()),
		"exit-sparkup-mode": (SSIGNAL, TYPE_NONE, ()),
		"next-placeholder": (SSIGNAL, TYPE_NONE, ()),
		"previous-placeholder": (SSIGNAL, TYPE_NONE, ()),
		"execute": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"inserted-template": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"placeholder-offsets": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"boundary-marks": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"placeholder-marks": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"cursor-in-placeholder": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"sparkup-template": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)

