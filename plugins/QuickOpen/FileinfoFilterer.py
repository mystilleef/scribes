class Filterer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("filter-fileinfos", self.__filter_cb)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__extensions = (
			"bmp", "tif", "tiff", "ps", "png", "mng", "ico", "jpg",
			"jpeg", "gif", "xcf", "pdf", "aac", "flac", "mp3",
			"ogg", "ra", "ram", "snd", "wav", "wma", "asf", "asx",
			"avi", "divx", "flv", "mov", "mp4", "mpeg", "mpg", "qt",
			"wmv", "xvid", "gdb", "dll", "ods", "pps", "ppsx", "ppt",
			"xls", "xlsx", "otf", "ttf", "cab", "la", "so", "lo", "o", "exe",
			"bat", "7z", "bz", "bz2", "bzip", "deb", "gz", "gzip",
			"rar", "zip", "tar", "tbz", "tbz2", "iso", "msi", "part",
			"torrent", "doc", "pyo", "pyc", "nfo", "m4v", "rtf", "in",
			"gmo", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
			"toc", "odt", "dat", "svg"
		)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __valid(self, fileinfo):
		self.__editor.response()
		if fileinfo.get_is_hidden(): return False
		if fileinfo.get_is_symlink(): return False
		if fileinfo.get_is_backup(): return False
		extension = fileinfo.get_display_name().split(".")[-1]
		if extension.lower() in self.__extensions: return False
		return True

	def __filter(self, data):
		self.__editor.response()
		folder, fileinfos = data
		fileinfos = [fileinfo for fileinfo in fileinfos if self.__valid(fileinfo)]
		self.__manager.emit("folder-and-fileinfos", (folder, fileinfos))
		return False

	def __optimize(self):
		self.__editor.optimize((self.__filter, self.__valid))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __filter_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__filter, data, priority=9999)
		return False
