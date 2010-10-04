from gettext import gettext as _

class FileChooser(object):

	def __init__(self, editor, manager):
		editor.response()
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__chooser.connect("file-activated", self.__file_activated_cb)
		self.__sigid3 = self.__chooser.connect("selection-changed", self.__selection_changed_cb)
		self.__sigid4 = self.__manager.connect("activate-chooser", self.__load_schemes_cb)
		self.__sigid5 = self.__manager.connect("show-add-schemes-window", self.__show_cb)
		self.__chooser.set_property("sensitive", True)
		editor.response()

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.dialog_gui.get_widget("FileChooser")
		return

	def __set_properties(self):
		from gtk import FileFilter
		filefilter = FileFilter()
		filefilter.set_name(_("Color Scheme Files"))
#		filefilter.add_mime_type("text/xml")
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
		self.__manager.emit("hide-add-schemes-window")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __validate(self):
		try:
			filenames = self.__chooser.get_filenames()
			if not filenames: raise ValueError
			from os.path import isdir
			is_a_folder = lambda _file: isdir(_file)
			folders = filter(is_a_folder, filenames)
			valid = False if folders else True
			self.__manager.emit("valid-selection", valid)
		except ValueError:
			self.__manager.emit("valid-selection", False)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __file_activated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_schemes)
		return False

	def __load_schemes_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_schemes)
		return

	def __selection_changed_cb(self, *args):
		self.__validate()
		return False

	def __show_cb(self, *args):
		self.__validate()
		return False
