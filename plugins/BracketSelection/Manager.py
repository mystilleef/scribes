from gobject import SIGNAL_RUN_LAST, SIGNAL_NO_RECURSE, SIGNAL_ACTION
from gobject import TYPE_NONE, GObject
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"select": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Selector import Selector
		Selector(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False

	def select(self):
		self.emit("select")
		return False
