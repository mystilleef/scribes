from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_BOOLEAN, TYPE_NONE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from BusyManager import Manager
		Manager(self, editor)
		from MessageLabel import Label
		Label(self, editor)
		from TitleLabel import Label
		Label(self, editor)
		from Image import Image
		Image(self, editor)
		from WindowTitleUpdater import Updater
		Updater(self, editor)
		from Window import Window
		Window(self, editor)

	def __init_attributes(self, editor):
		self.__glade = editor.get_glade_object(globals(), "MessageWindow.glade", "Window")
		return

	gui = property(lambda self: self.__glade)
