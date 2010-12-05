from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"check": (SSIGNAL, TYPE_NONE, ()),
		"start-check": (SSIGNAL, TYPE_NONE, ()),
		"remote-file-error": (SSIGNAL, TYPE_NONE, ()),
		"remote-file-message": (SSIGNAL, TYPE_NONE, ()),
		"check-message": (SSIGNAL, TYPE_NONE, ()),
		"error-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"error-check-type": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-updated": (SSIGNAL, TYPE_NONE, ()),
		"toggle-error-check": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
