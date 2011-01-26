from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"inserting-text": (SSIGNAL, TYPE_NONE, ()),
		"inserted-text": (SSIGNAL, TYPE_NONE, ()),
		"database-updated": (SSIGNAL, TYPE_NONE, ()),
		"index": (SSIGNAL, TYPE_NONE, ()),
		"enable-word-completion": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"update-database": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"dictionary": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"match-found": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"no-match-found": (SSIGNAL, TYPE_NONE, ()),
		"valid-string": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"invalid-string": (SSIGNAL, TYPE_NONE, ()),
		"hide-window": (SSIGNAL, TYPE_NONE, ()),
		"show-window": (SSIGNAL, TYPE_NONE, ()),
		"treeview-size": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"insertion-marks": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"insert-text": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"generate": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
