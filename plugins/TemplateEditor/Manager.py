from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION, TYPE_STRING
from gobject import TYPE_BOOLEAN
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-import-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-import-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-export-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-export-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"selected-language-id": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"language-treeview-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"language-treeview-cursor-changed": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"description-treeview-cursor-changed": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"description-treeview-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"description-treeview-sensitivity": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"templates-dictionary": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"template-triggers": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"gui-template-editor-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-template-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-template-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"process-imported-files": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"valid-template-files": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"imported-templates-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"validate-imported-templates": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-imported-templates": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-templates-dictionary-key": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"selected-templates-dictionary-keys": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"select-description-treeview": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"show-add-template-editor": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"remove-selected-templates": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-edit-template-editor": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-template-editor": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"ready": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"validator-is-ready": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"updating-database": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"database-update": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"import-button-clicked": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"export-button-clicked": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"populated-description-treeview": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"created-template-file": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"created-xml-template-file": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"name-entry-string": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"error": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"valid-trigger": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"can-import-selected-file": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"select-language-treeview-id": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"export-template-filename": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"export-template-data": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"validate-export-template-path": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
		"create-export-template-filename": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Import.Manager import Manager
		Manager(self, editor)
		from Export.Manager import Manager
		Manager(self, editor)
		from EditorGUI.Manager import Manager
		Manager(self, editor)
		from MainGUI.Manager import Manager
		Manager(self, editor)
		from DatabaseUpdater import Updater
		Updater(self, editor)
		# This Monitor object should be initialized last.
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		self.__glade = editor.get_glade_object(globals(), join("MainGUI", "GUI.glade"), "Window")
		self.__eglade = editor.get_glade_object(globals(), join("EditorGUI", "GUI.glade"), "Window")
		self.__iglade = editor.get_glade_object(globals(), join("Import", "GUI", "GUI.glade"), "Window")
		self.__exglade = editor.get_glade_object(globals(), join("Export", "GUI", "GUI.glade"), "Window")
		return

	gui = property(lambda self: self.__glade)
	editor_gui = property(lambda self: self.__eglade)
	import_gui = property(lambda self: self.__iglade)
	export_gui = property(lambda self: self.__exglade)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False

	def show(self):
		self.emit("show-window")
		return False
