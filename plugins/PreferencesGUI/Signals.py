from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"updated-language-combobox": (SSIGNAL, TYPE_NONE, ()),
		"language-combobox-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-language": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"sensitive": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"margin-display": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-update": (SSIGNAL, TYPE_NONE, ()),
		"reset": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
