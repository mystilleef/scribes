class FileChooser(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect_after("show-open-dialog-window", self.__show_window_cb)
		self.__sigid2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__chooser.connect("file-activated", self.__file_activated_cb)
		self.__sigid4 = self.__chooser.connect("selection-changed", self.__selection_changed_cb)
		self.__sigid5 = self.__manager.connect("load-files", self.__load_files_cb)
		self.__sigid6 = self.__manager.connect("open-encoding", self.__encoding_cb)
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.open_gui.get_widget("FileChooser")
		self.__encoding = None
		return

	def __set_properties(self):
		for filter_ in self.__editor.dialog_filters:
			self.__editor.response()
			self.__chooser.add_filter(filter_)
		self.__set_folder()
		return

	def __set_folder(self):
		if not (self.__editor.uri): return False
		self.__chooser.set_uri(self.__editor.uri)
		return False

	def __load_uris(self):
		self.__manager.emit("hide-open-dialog-window")
		encoding = self.__encoding if self.__encoding else "utf8"
		uris = self.__chooser.get_uris()
		self.__manager.emit("open-files", uris, encoding)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid4, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __show_window_cb(self, *args):
		self.__set_folder()
		return

	def __file_activated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_uris)
		return False

	def __load_files_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_uris)
		return

	def __encoding_cb(self, manager, encoding):
		self.__encoding = encoding
		return False

	def __selection_changed_cb(self, *args):
		uris = self.__chooser.get_uris()
		if not uris: return False
		folders = [uri for uri in uris if self.__editor.uri_is_folder(uri)]
		selected_file = False if folders else True
		self.__manager.emit("open-button-sensitivity", selected_file)
		return False
