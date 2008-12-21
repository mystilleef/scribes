from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject, TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"scan-schemes": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"populated-model": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"schemes": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"treeview-data": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"current-scheme": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-scheme": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-scheme": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
#		from RemoveButton import RemoveButton
#		RemoveButton(editor, self)
#		from AddButton import AddButton
#		AddButton(editor, self)
		from SchemeChanger import Changer
		Changer(editor, self)
		from CurrentSchemeMonitor import Monitor
		Monitor(editor, self)
		from Window import Window
		Window(editor, self)
		from TreeView import TreeView
		TreeView(editor, self)
		from TreeViewDataGenerator import Generator
		Generator(editor, self)
		from SchemeDispatcher import Dispatcher
		Dispatcher(editor, self)
		self.emit("scan-schemes")

	def __init_attributes(self, editor):
		self.__glade = editor.get_glade_object(globals(), "SyntaxColorThemes.glade", "Window")
		return

	gui = property(lambda self: self.__glade)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def show(self):
		self.emit("show-window")
		return
