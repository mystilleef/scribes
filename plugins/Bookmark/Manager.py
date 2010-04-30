from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"toggle-bookmark": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"remove-all-bookmarks": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"marked-lines": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"scroll-to-line": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"populate-model": (SCRIBES_SIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"gui-created": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"show-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
		"hide-window": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from MarkNavigator import Navigator
		Navigator(self, editor)
		from MarginDisplayer import Displayer
		Displayer(self, editor)
		from DatabaseUpdater import Updater
		Updater(self, editor)
		from BufferMonitor import Monitor
		Monitor(self, editor)
		from BufferMarker import Marker
		Marker(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		self.__glade = editor.get_glade_object(globals(), join("GUI","Bookmark.glade"), "Window")
		self.__browser = None
		return False

	def destroy(self):
		if self.__browser: self.__browser.destroy()
		self.emit("destroy")
		del self
		self = None
		return

	gui = property(lambda self: self.__glade)

	def toggle(self):
		self.emit("toggle-bookmark")
		return False

	def remove(self):
		self.emit("remove-all-bookmarks")
		return False

	def show(self, *args):
		try:
			self.__browser.show()
		except AttributeError:
			from GUI.Manager import Manager
			self.__browser = Manager(self, self.__editor)
			self.__browser.show()
		return False
