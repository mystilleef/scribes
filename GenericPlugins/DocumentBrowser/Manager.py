from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"update": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"get-uris": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Window import Window
		Window(editor, self)
		from TreeView import TreeView
		TreeView(editor, self)
		from Updater import Updater
		Updater(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "DocumentBrowser.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	glade = property(lambda self: self.__glade)

	def show(self):
		self.emit("get-uris")
		self.emit("show-window")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		return
