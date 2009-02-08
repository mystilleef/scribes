class FileChooser(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("export-template-filename", self.__export_template_filename_cb)
		self.__sigid3 = manager.connect("export-button-clicked", self.__export_button_clicked_cb)
		self.__set_folder()
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.export_gui.get_widget("FileChooser")
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
		set_folder = self.__chooser.set_current_folder
		desktop = self.__editor.desktop_folder
		home = self.__editor.home_folder
		from os.path import exists
		set_folder(desktop) if exists(desktop) else set_folder(home)
		self.__chooser.grab_focus()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __emit_template_path_signal(self):
		filename = self.__chooser.get_filename()
		self.__manager.emit("validate-export-template-path", filename)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __export_template_filename_cb(self, manager, filename):
		self.__chooser.set_current_name(filename)
		return False

	def __export_button_clicked_cb(self, *args):
		self.__emit_template_path_signal()
		return False
