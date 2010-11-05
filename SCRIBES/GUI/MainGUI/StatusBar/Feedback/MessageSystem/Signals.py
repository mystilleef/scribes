from SCRIBES.SIGNALS import GObject, TYPE_NONE, SSIGNAL, TYPE_PYOBJECT

class Signal(GObject):

	__gsignals__ = {
		"message-bar-is-updated": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"reset": (SSIGNAL, TYPE_NONE, ()),
		"fallback": (SSIGNAL, TYPE_NONE, ()),
		"update-message-bar": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"format-feedback-message": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"busy": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
