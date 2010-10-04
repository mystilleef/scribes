from SCRIBES.SIGNALS import GObject, TYPE_NONE, TYPE_PYOBJECT, SSIGNAL

class Signal(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"deactivate": (SSIGNAL, TYPE_NONE, ()),
		"toggle-edit-point": (SSIGNAL, TYPE_NONE, ()),
		"add-edit-point": (SSIGNAL, TYPE_NONE, ()),
		"remove-edit-point": (SSIGNAL, TYPE_NONE, ()),
		"no-edit-point-error": (SSIGNAL, TYPE_NONE, ()),
		"backspace": (SSIGNAL, TYPE_NONE, ()),
		"delete": (SSIGNAL, TYPE_NONE, ()),
		"clear": (SSIGNAL, TYPE_NONE, ()),
		"column-mode-reset": (SSIGNAL, TYPE_NONE, ()),
		"edit-points": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"column-edit-point": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"inserted-text": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"add-mark": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-mark": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"smart-column-edit-point": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self):
		GObject.__init__(self)
