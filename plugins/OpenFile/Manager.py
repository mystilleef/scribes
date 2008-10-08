from gobject import GObject, TYPE_NONE, SIGNAL_RUN_LAST, TYPE_PYOBJECT
from gobject import TYPE_STRING, TYPE_BOOLEAN

class Manager(GObject):
	
	__gsignals__ = {
		"show-open-dialog-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-open-dialog-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-remote-dialog-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-newfile-dialog-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-newfile-dialog-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"open-files": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT, TYPE_STRING)),
		"open-button-sensitivity": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_BOOLEAN,)),
		"load-files": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"open-encoding": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"validate": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"validation-error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"validation-pass": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"create": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"create-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"creation-error": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
		"creation-pass": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from FileOpener import Opener
		Opener(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		pwd = editor.get_current_folder(globals())
		from os.path import join
		file_ = join(pwd, "OpenDialogGUI/OpenDialog.glade")
		from gtk.glade import XML
		self.__oglade = XML(file_, "Window", "scribes")
		file_ = join(pwd, "NewFileDialogGUI/NewFileDialog.glade")
		self.__nglade = XML(file_, "Window", "scribes")
		self.__open_manager = None
		self.__remote_manager = None
		self.__newfile_manager = None
		return False

	open_gui = property(lambda self: self.__oglade)
	new_gui = property(lambda self: self.__nglade)

	def show_open_dialog(self):
		try:
			self.__open_manager.show()
		except AttributeError:
			from OpenDialogGUI.Manager import Manager
			self.__open_manager = Manager(self, self.__editor)
			self.__open_manager.show()
		return

	def show_remote_dialog(self):
		self.emit("show-remote-dialog-window")
		return 

	def show_newfile_dialog(self):
		try:
			self.__new_manager.show()
		except AttributeError:
			from NewFileDialogGUI.Manager import Manager
			self.__new_manager = Manager(self, self.__editor)
			self.__new_manager.show()
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
