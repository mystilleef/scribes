from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"hide-window": (SSIGNAL, TYPE_NONE, ()),
		"show-window": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"updated-model": (SSIGNAL, TYPE_NONE, ()),
		"selected-row": (SSIGNAL, TYPE_NONE, ()),
		"hide-message": (SSIGNAL, TYPE_NONE, ()),
		"up-key-press": (SSIGNAL, TYPE_NONE, ()),
		"shift-up-key-press": (SSIGNAL, TYPE_NONE, ()),
		"down-key-press": (SSIGNAL, TYPE_NONE, ()),
		"shift-down-key-press": (SSIGNAL, TYPE_NONE, ()),
		"focus-entry": (SSIGNAL, TYPE_NONE, ()),
		"activate-selected-rows": (SSIGNAL, TYPE_NONE, ()),
		"recent-infos": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"model-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"recent-infos-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"filtered-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"open-files": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-pattern": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"message": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
