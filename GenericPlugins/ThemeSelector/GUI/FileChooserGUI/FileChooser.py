from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class FileChooser(SignalManager):

	def __init__(self, editor, manager):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__chooser, "file-activated", self.__activated_cb)
		self.connect(self.__chooser, "selection-changed", self.__changed_cb)
		self.connect(manager, "activate-chooser", self.__load_schemes_cb)
		self.connect(manager, "show-chooser", self.__show_cb)
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.chooser_gui.get_object("FileChooser")
		return

	def __set_properties(self):
		from gtk import FileFilter
		filefilter = FileFilter()
		filefilter.set_name(_("Color Scheme Files"))
		filefilter.add_pattern("*.xml")
		self.__chooser.add_filter(filefilter)
		self.__set_folder()
		return

	def __set_folder(self):
		from os.path import exists
		if exists(self.__editor.desktop_folder):
			self.__chooser.set_current_folder(self.__editor.desktop_folder)
		else:
			self.__chooser.set_current_folder(self.__editor.home_folder)
		return False

	def __load_schemes(self):
		filenames = self.__chooser.get_filenames()
		self.__manager.emit("process-xml-files", filenames)
		self.__manager.emit("hide-chooser")
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __validate(self):
		try:
			filenames = self.__chooser.get_filenames()
			if not filenames: raise ValueError
			from os.path import isdir
			is_a_folder = lambda _file: isdir(_file)
			folders = filter(is_a_folder, filenames)
			valid = False if folders else True
			self.__manager.emit("valid-chooser-selection", valid)
		except ValueError:
			self.__manager.emit("valid-chooser-selection", False)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __activated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_schemes)
		return False

	def __load_schemes_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_schemes)
		return

	def __changed_cb(self, *args):
		self.__validate()
		return False

	def __show_cb(self, *args):
		self.__validate()
		return False
