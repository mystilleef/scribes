from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"new-job": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"syntax-check": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"flakes-check": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"pylint-check": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"pycheck": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"stop": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"ignored": (SSIGNAL, TYPE_NONE, ()), 
	}

	def __init__(self):
		GObject.__init__(self)
