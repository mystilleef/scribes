from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import TYPE_BOOLEAN

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"loaded-language-templates": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"loaded-general-templates": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"trigger-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"no-trigger-found": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"trigger-activated": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"template-destroyed": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"template-boundaries": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"next-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"previous-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"expand-trigger": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"deactivate-template-mode": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"activate-template-mode": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy-template": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"last-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"placeholders": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"tag-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-placeholder": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-update": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"reformat-template": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from TriggerColorer import Colorer
		Colorer(editor, self)
		from TemplateDeactivator import Deactivator
		Deactivator(editor, self)
		from PlaceholderColorer import Colorer
		Colorer(editor, self)
		from PlaceholderNavigator import Navigator
		Navigator(editor, self)
		from TriggerMonitor import Monitor
		Monitor(editor, self)
		from TemplateInserter import Inserter
		Inserter(editor, self)
		from Loader import Loader
		Loader(editor, self)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		from TemplateIndentationDatabaseListener import Listener
		Listener(self, editor)
		editor.response()

	def __destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return
