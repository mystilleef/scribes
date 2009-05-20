from gettext import gettext as _

class FileChooser(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__chooser.connect("file-activated", self.__activated_cb)
		self.__sigid3 = self.__chooser.connect("selection-changed", self.__changed_cb)
		self.__sigid4 = manager.connect("import-button-clicked", self.__activated_cb)
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.import_gui.get_widget("FileChooser")
		self.__can_import = True
		return

	def __set_properties(self):
		from gtk import FileFilter
		filter_ = FileFilter()
		filter_.set_name(_("Template Files"))
		filter_.add_mime_type("text/xml")
		self.__chooser.add_filter(filter_)
		self.__set_folder()
		return

	def __set_folder(self):
		from os.path import exists
		if exists(self.__editor.desktop_folder):
			self.__chooser.set_current_folder(self.__editor.desktop_folder)
		else:
			self.__chooser.set_current_folder(self.__editor.home_folder)
		self.__chooser.grab_focus()
		return

	def __import_templates(self):
		filenames = self.__chooser.get_filenames()
		self.__manager.emit("hide-import-window")
		self.__manager.emit("process-imported-files", filenames)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __activated_cb(self, *args):
		self.__import_templates()
		return True

	def __changed_cb(self, *args):
		uris = self.__chooser.get_uris()
		if not uris: return False
		is_a_folder = lambda _file: self.__editor.uri_is_folder(_file)
		folders = filter(is_a_folder, uris)
		self.__can_import = False if folders else True
		self.__manager.emit("can-import-selected-file", self.__can_import)
		return False
