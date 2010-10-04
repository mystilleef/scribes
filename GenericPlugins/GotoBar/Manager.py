from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_INT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-bar": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-bar": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"line-number": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_INT,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(editor)
		from LineJumper import Jumper
		Jumper(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		from os.path import join
		folder = editor.get_current_folder(globals())
		file_ = join(folder, "GUI/GotoBar.glade")
		from gtk.glade import XML
		self.__glade = XML(file_, "Window", "scribes")
		return

	gui = property(lambda self: self.__glade)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def show(self):
		self.emit("show-bar")
		return
