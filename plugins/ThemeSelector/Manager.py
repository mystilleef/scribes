from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject, TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"can-remove": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-theme": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"folder-changed": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"focus-treeview": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
#		from RemoveButton import RemoveButton
#		RemoveButton(editor, self)
#		from AddButton import AddButton
#		AddButton(editor, self)
#		from TreeView import TreeView
#		TreeView(editor, self)
		from Window import Window
		Window(editor, self)
#		from SchemeMonitor import Monitor
#		Monitor(editor, self)

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
