from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"comment-boundary": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"single-line-boundary": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"multiline-boundary": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"processed-text": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"inserted-text": (SSIGNAL, TYPE_NONE, ()),
		"finished": (SSIGNAL, TYPE_NONE, ()),
		"commenting": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
