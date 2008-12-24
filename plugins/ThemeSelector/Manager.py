from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject, TYPE_PYOBJECT
from gobject import TYPE_BOOLEAN

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
		"process-xml-files": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"valid-scheme-files": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"activate-chooser": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"remove-button-sensitivity": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"valid-selection": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"remove-row": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-add-schemes-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-add-schemes-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from SchemeFileInstaller import Installer
		Installer(editor, self)
		from SchemeFileValidator import Validator
		Validator(editor, self)
		from AddSchemesGUI.Manager import Manager
		Manager(editor, self)
		from RemoveButton import Button
		Button(editor, self)
		from AddButton import Button
		Button(editor, self)
		from SchemeRemover import Remover
		Remover(editor, self)
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
		from SchemesFolderMonitor import Monitor
		Monitor(editor, self)

	def __init_attributes(self, editor):
		self.__glade = editor.get_glade_object(globals(), "SyntaxColorThemes.glade", "Window")
		self.__dialog = editor.get_glade_object(globals(), "AddSchemesGUI/Dialog.glade", "Window")
		return

	gui = property(lambda self: self.__glade)
	dialog_gui = property(lambda self: self.__dialog)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def show(self):
		self.emit("show-window")
		return
