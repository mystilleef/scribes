from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import TYPE_BOOLEAN, TYPE_STRING

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"encoding": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"rename": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from ComboBox import ComboBox
		ComboBox(self, editor)
		from SaveButton import Button
		Button(editor, self)
		from FileChooser import FileChooser
		FileChooser(editor, self)
		from CancelButton import Button
		Button(editor, self)
		from Window import Window
		Window(editor, self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.get_current_folder(globals()), "SaveDialog.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	gui = property(lambda self: self.__glade)

	def show(self):
		self.emit("show-window")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
