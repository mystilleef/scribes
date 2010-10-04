from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"toggle": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"remove-all": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"add": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"lines": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"bookmark-lines": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"feedback": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"model-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"scroll-to-line": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"updated-model": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
