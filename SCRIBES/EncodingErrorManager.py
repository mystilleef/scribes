from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_STRING
from gobject import TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"encoding-data": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-encoding": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"load": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"quit": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from EncodingErrorWindow import Window
		Window(self, editor)
		from EncodingErrorTitleLabel import Label
		Label(self, editor)
		from EncodingErrorComboBox import ComboBox
		ComboBox(self, editor)
		from EncodingErrorLoader import Loader
		Loader(self, editor)
		from EncodingErrorOpenButton import Button
		Button(self, editor)
		from EncodingErrorCloseButton import Button
		Button(self, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("private-encoding-load-error", self.__encoding_error_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.data_folder, "EncodingErrorWindow.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __destroy(self):
		self.emit("quit")
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__glade.get_widget("Window").destroy()
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	glade = property(lambda self: self.__glade)

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __encoding_error_cb(self, *args):
		self.emit("show-window")
		return False
