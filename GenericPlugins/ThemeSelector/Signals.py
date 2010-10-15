from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"database-update": (SSIGNAL, TYPE_NONE, ()),
		"show-window": (SSIGNAL, TYPE_NONE, ()),
		"hide-window": (SSIGNAL, TYPE_NONE, ()),
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"updated-model": (SSIGNAL, TYPE_NONE, ()),
		"theme-folder-update": (SSIGNAL, TYPE_NONE, ()),
		"selected-row": (SSIGNAL, TYPE_NONE, ()),
		"update-database": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"theme-from-database": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"schemes": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-scheme": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"model-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"last-selected-path": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"ignore-row-activation": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"delete-row": (SSIGNAL, TYPE_NONE, ()),
		"delete-error": (SSIGNAL, TYPE_NONE, ()),
		"row-changed": (SSIGNAL, TYPE_NONE, ()),
		"remove-scheme": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"message": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"valid-scheme-files": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"process-xml-files": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"valid-chooser-selection": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"treeview-sensitivity": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"invalid-scheme-files": (SSIGNAL, TYPE_NONE, ()),
		"hide-message": (SSIGNAL, TYPE_NONE, ()),
		"show-chooser": (SSIGNAL, TYPE_NONE, ()),
		"hide-chooser": (SSIGNAL, TYPE_NONE, ()),
		"activate-chooser": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self):
		GObject.__init__(self)
