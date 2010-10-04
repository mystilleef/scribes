from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import TYPE_PYOBJECT, SIGNAL_NO_RECURSE, SIGNAL_ACTION
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"activate": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(editor)
		from SmartSpace import SmartSpace
		SmartSpace(editor, self)
		from ConfigurationManager import Manager
		Manager(editor, self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
