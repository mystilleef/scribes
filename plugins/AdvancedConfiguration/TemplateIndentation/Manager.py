from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_BOOLEAN
from gobject import TYPE_NONE
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"set-data": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"get-data": (SSIGNAL, TYPE_NONE, (TYPE_BOOLEAN,)),
		"destroy": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, manager, editor):
		editor.response()
		GObject.__init__(self)
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from DatabaseUpdater import Updater
		Updater(self, editor)
		from CheckButton import Button
		Button(self, editor)
		from DatabaseListener import Listener
		Listener(self, editor)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__gui = manager.gui
		return

	def __destroy(self):
		self.emit("destroy")
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		del self
		self = None
		return False

	# Public API reference to the advanced configuration window GUI
	gui = property(lambda self: self.__gui)

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
