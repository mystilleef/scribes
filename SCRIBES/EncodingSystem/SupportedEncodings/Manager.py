from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE, TYPE_PYOBJECT
from gobject import TYPE_OBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"activate": (SSIGNAL, TYPE_NONE, ()),
		"database-changed": (SSIGNAL, TYPE_NONE, ()),
		"encoding-list": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-encodings": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"model-data": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"updated-model": (SSIGNAL, TYPE_NONE, ()),
		"toggled-path": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from EncodingListDispatcher import Dispatcher
		Dispatcher(self, editor)
		from EncodingListDatabaseMonitor import Monitor
		Monitor(self, editor)
		from EncodingListDatabaseUpdater import Updater
		Updater(self, editor)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__gui = editor.get_glade_object(globals(), "GUI/GUI.glade", "Window")
		return

	gui = property(lambda self: self.__gui)

	def activate(self):
		self.emit("activate")
		return False

	def destroy(self):
		del self
		return False
