from gobject import SIGNAL_RUN_LAST, SIGNAL_ACTION, SIGNAL_NO_RECURSE
from gobject import TYPE_NONE, GObject
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Window import Window
		Window(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__glade = editor.get_glade_object(globals(), "Preferences.glade", "Window")
		return

	def __destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	gui = property(lambda self: self.__glade)

	def show(self):
		self.emit("show-window")
		return

	def destroy(self):
		self.__destroy()
		return
