from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_ACTION, SIGNAL_NO_RECURSE
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"process-fileinfo": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"fileinfo": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}
	

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(editor)
		from FileInfo import FileInfo
		FileInfo(self, editor)
		from Window import Window
		Window(self, editor)
		from NameLabel import Label
		Label(self, editor)
		from TypeLabel import Label
		Label(self, editor)
		from SizeLabel import Label
		Label(self, editor)
		from LocationLabel import Label
		Label(self, editor)
		from MIMELabel import Label
		Label(self, editor)
		from LinesLabel import Label
		Label(self, editor)
		from WordsLabel import Label
		Label(self, editor)
		from CharactersLabel import Label
		Label(self, editor)
		from ModifiedLabel import Label
		Label(self, editor)
		from AccessedLabel import Label
		Label(self, editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__glade = editor.get_glade_object(globals(), "DocumentStatistics.glade", "Window")
		return

	glade = property(lambda self: self.__glade)

	def show(self):
		self.emit("process-fileinfo")
		self.emit("show-window")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
