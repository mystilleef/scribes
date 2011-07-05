from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"updated-model": (SSIGNAL, TYPE_NONE, ()),
		"go-back": (SSIGNAL, TYPE_NONE, ()),
		"go-up": (SSIGNAL, TYPE_NONE, ()),
		"go-home": (SSIGNAL, TYPE_NONE, ()),
		"show-hidden": (SSIGNAL, TYPE_NONE, ()),
		"hide-hidden": (SSIGNAL, TYPE_NONE, ()),
		"showing-browser": (SSIGNAL, TYPE_NONE, ()),
		"hiding-browser": (SSIGNAL, TYPE_NONE, ()),
		"toggle-hidden": (SSIGNAL, TYPE_NONE, ()),
		"switch-focus": (SSIGNAL, TYPE_NONE, ()),
		"gained-focus": (SSIGNAL, TYPE_NONE, ()),
		"lost-focus": (SSIGNAL, TYPE_NONE, ()),
		"activate-selection": (SSIGNAL, TYPE_NONE, ()),
		"dummy-signal": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"generate-uris": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"generate-uris-for-treenode": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished-generating-uris": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"treeview-model-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"generate-data-for-treeview": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"generating-data-for-treeview": (SSIGNAL, TYPE_NONE, ()),
		"history-depth": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"enumerate-children": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"finished-enumerating-children": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"history-depth": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
