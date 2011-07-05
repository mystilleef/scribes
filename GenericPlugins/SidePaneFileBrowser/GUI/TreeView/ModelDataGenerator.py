from SCRIBES.SignalConnectionManager import SignalManager

EXTENSIONS = (
	"bmp", "tif", "tiff", "ps", "png", "mng", "ico", "jpg",
	"jpeg", "gif", "xcf", "pdf", "aac", "flac", "mp3",
	"ogg", "ra", "ram", "snd", "wav", "wma", "asf", "asx",
	"avi", "divx", "flv", "mov", "mp4", "mpeg", "mpg", "qt",
	"wmv", "xvid", "gdb", "dll", "ods", "pps", "ppsx", "ppt",
	"xls", "xlsx", "otf", "ttf", "cab", "la", "so", "lo", "o", "exe",
	"bat", "7z", "bz", "bz2", "bzip", "deb", "gz", "gzip",
	"rar", "zip", "tar", "tbz", "tbz2", "iso", "msi", "part",
	"torrent", "doc", "pyo", "pyc", "nfo", "m4v", "rtf", "rpm",
	"gmo", "toc", "odt", "dat", "svg", "xz"
)

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "generate-data-for-treeview", self.__generate_cb)
		self.connect(manager, "show-hidden", self.__show_cb)
		self.connect(manager, "hide-hidden", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__show_hidden = False
		self.__data = None
		from gtk import icon_theme_get_default
		self.__icon_theme = icon_theme_get_default()
		self.__icons = self.__icon_theme.list_icons()
		return

	def __generate(self, data):
		from gobject import idle_add
		idle_add(self.__manager.emit, "generating-data-for-treeview")
		folder_uri, fileinfos, treeview_iterator = data
		folders = (fileinfo for fileinfo in fileinfos if self.__is_folder(fileinfo))
		files = (fileinfo for fileinfo in fileinfos if self.__is_file(fileinfo))
		folders = (self.__fileinfo(fileinfo, folder_uri, "folder") for fileinfo in folders)
		files = (self.__fileinfo(fileinfo, folder_uri) for fileinfo in files)
		# Filter out files that are not in EXTENSIONS
		files = (file_data for file_data in files if file_data[1].lower().split(".")[-1] not in EXTENSIONS)
		idle_add(self.__manager.emit, "treeview-model-data", (sorted(folders), sorted(files), treeview_iterator))
		return False

	def __is_folder(self, fileinfo):
		file_type = fileinfo.get_file_type()
		is_hidden = fileinfo.get_is_hidden()
		if is_hidden and self.__show_hidden is False: return False
		from gio import FILE_TYPE_DIRECTORY
		return file_type == FILE_TYPE_DIRECTORY

	def __is_file(self, fileinfo):
		file_type = fileinfo.get_file_type()
		is_hidden = fileinfo.get_is_hidden()
		if is_hidden and self.__show_hidden is False: return False
		from gio import FILE_TYPE_REGULAR
		return file_type == FILE_TYPE_REGULAR

	def __fileinfo(self, fileinfo, folder_uri, file_type="file"):
		name = fileinfo.get_name()
		from gio import File
		uri = File(folder_uri).resolve_relative_path(name).get_uri()
		display_name = fileinfo.get_display_name()
		return uri, display_name, fileinfo.get_icon(), file_type

	def __generate_cb(self, manager, data):
		self.__data = data
		from gobject import idle_add
		idle_add(self.__generate, data)
		return False

	def __show_cb(self, *args):
		self.__show_hidden = True
		from gobject import idle_add
		idle_add(self.__generate, self.__data)
		return False

	def __hide_cb(self, *args):
		self.__show_hidden = False
		from gobject import idle_add
		idle_add(self.__generate, self.__data)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
