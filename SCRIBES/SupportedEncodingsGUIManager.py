from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_BOOLEAN
from gobject import TYPE_STRING, TYPE_PYOBJECT, TYPE_OBJECT

class Manager(GObject):

	__gsignals__ = {
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_OBJECT,)),
		"quit": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"new-encoding": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING, TYPE_BOOLEAN)),
		"encoding-list": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from SupportedEncodingsWindow import Window
		Window(self, editor)
		from SupportedEncodingsTreeView import TreeView
		TreeView(self, editor)
		from SupportedEncodingsDatabaseManager import Manager
		Manager(self, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("supported-encodings-window", self.__show_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.data_folder, "EncodingSelectionWindow.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __destroy(self):
		self.emit("quit")
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	glade = property(lambda self: self.__glade)

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, editor, window):
		self.emit("show-window", window)
		return False
