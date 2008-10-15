from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_INT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"line-number": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_INT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from LineJumper import Jumper
		Jumper(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)

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
