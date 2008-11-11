from gobject import SIGNAL_ACTION, SIGNAL_RUN_LAST, TYPE_NONE, GObject
from gobject import SIGNAL_NO_RECURSE, TYPE_PYOBJECT
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"selected-placeholder": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from BracketSelectionColorButton import ColorButton
		ColorButton(editor, self)
		from Window import Window
		Window(editor, self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join, split
		current_folder = editor.get_current_folder(globals())
		glade_file = join(current_folder, "AdvancedConfigurationWindow.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	# Public API reference to the advanced configuration window GUI
	gui = property(lambda self: self.__glade)

	def show(self):
		self.emit("show-window")
		return

	def destroy(self):
		self.__destroy()
		return
