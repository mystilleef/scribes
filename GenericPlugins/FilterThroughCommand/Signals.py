from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"win": (SSIGNAL, TYPE_NONE, ()),
		"fail": (SSIGNAL, TYPE_NONE, ()),
		"execute": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"mapped": (SSIGNAL, TYPE_NONE, ()),
		"restored-cursor-position": (SSIGNAL, TYPE_NONE, ()),
		"database-updated": (SSIGNAL, TYPE_NONE, ()),
		"result": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"bounds": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"command": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"output-mode": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update-database": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
