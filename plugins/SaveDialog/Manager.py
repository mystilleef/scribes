from SCRIBES.SIGNALS import SSIGNAL, TYPE_NONE, TYPE_PYOBJECT, GObject

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SSIGNAL, TYPE_NONE, ()),
		"show": (SSIGNAL, TYPE_NONE, ()),
		"hide": (SSIGNAL, TYPE_NONE, ()),
		"encoding": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"change-folder": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"validate": (SSIGNAL, TYPE_NONE, ()),
		"rename": (SSIGNAL, TYPE_NONE, ()),
		"save-button-activate": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Renamer import Renamer
		Renamer(self, editor)
		from NameValidator import Validator
		Validator(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)

	def __init_attributes(self, editor):
		self.__gui = editor.get_gui_object(globals(), "GUI/GUI.glade")
		return

	gui = property(lambda self: self.__gui)

	def show(self):
		self.emit("show")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
