from gettext import gettext as _

class FileChooser(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect_after("show-window", self.__show_cb)
		self.__sigid2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__manager.connect("rename", self.__rename_file_cb)
		self.__sigid4 = self.__manager.connect("encoding", self.__encoding_cb)
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.gui.get_widget("FileChooser")
		self.__encoding = "utf8"
		return

	def __set_properties(self):
		for filter_ in self.__editor.dialog_filters:
			self.__chooser.add_filter(filter_)
		self.__set_folder()
		return

	def __set_folder(self):
		if self.__editor.uri:
			from gnomevfs import URI, get_local_path_from_uri
			folder_uri = str(URI(self.__editor.uri).parent)
			current_name = str(URI(self.__editor.uri).short_name)
			if folder_uri != self.__chooser.get_current_folder_uri():
				self.__chooser.set_current_folder_uri(folder_uri)
			self.__chooser.set_current_name(current_name)
		else:
			self.__chooser.set_current_name(_("Unsaved Document"))
			self.__chooser.set_current_folder(self.__editor.desktop_folder)
		return False

	def __rename_file(self):
		from Exceptions import DialogError
		try:
			error = self.__validate_error()
			if error: raise DialogError
			self.__manager.emit("hide-window")
			uri = self.__chooser.get_uri()
			self.__editor.rename_file(uri, self.__encoding)
		except DialogError:
			title = "Validation Error"
			message = "The name in the text entry is not valid. Please make sure it is not a folder and it is a valid UNIX name."
			window = self.__manager.gui.get_widget("Window")
			self.__editor.show_error(title, message, window)
		return False

	def __validate_error(self):
		from gnomevfs import NotFoundError
		try:
			uri = self.__chooser.get_uri()
			if not uri: return True
			from gnomevfs import URI
			text = str(URI(uri).short_name)
			if not text: return True
			if "/" in text: return True
			if len(text) > 256: return True
			if self.__editor.uri_is_folder(uri): return True
		except NotFoundError:
			self.__editor.create_uri(uri)
			self.__validate_error()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __show_cb(self, *args):
		self.__set_folder()
		return

	def __rename_file_cb(self, *args):
		self.__rename_file()
		return

	def __encoding_cb(self, manager, encoding):
		self.__encoding = encoding
		return False
