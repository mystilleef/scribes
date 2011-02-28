from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"inserted-text": (SSIGNAL, TYPE_NONE, ()),
		"finished": (SSIGNAL, TYPE_NONE, ()),
		"region-marks": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"comment": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"uncomment": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"processed": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)

