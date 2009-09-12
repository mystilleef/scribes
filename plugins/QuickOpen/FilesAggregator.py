#FIXME: This module needs refactoring

class Aggregator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-path", self.__patch_cb)
		self.__sigid3 = manager.connect("folder-and-fileinfos", self.__fileinfos_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__folders = deque()
		self.__files = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __get_uri(self, folder, fileinfo):
		self.__editor.response()
		from gio import File 
		from os.path import join
		path = join(File(folder).get_path(), fileinfo.get_name())
		return File(path).get_uri()

	def __aggregate(self):
		files = []
		for folder, fileinfos in self.__files:
			self.__editor.response()
			for fileinfo in fileinfos:
				self.__editor.response()
				if fileinfo.get_is_backup() or fileinfo.get_is_symlink() or fileinfo.get_is_hidden(): continue
				if fileinfo.get_display_name().endswith(".pyo"): continue
				files.append(self.__get_uri(folder, fileinfo))
		self.__manager.emit("files", files)
		self.__files = []
		self.__folders = []
		return False

	def __get_files(self, data):
		folder, fileinfos = data
		self.__folders.remove(folder)
		_folders = []
		_fileinfos = []
		for fileinfo in fileinfos:
			self.__editor.response()
			if fileinfo.get_file_type() == 1: _fileinfos.append(fileinfo)
			if fileinfo.get_file_type() == 2: _folders.append(fileinfo)
		self.__files.append((folder, _fileinfos))
		[self.__process(self.__get_uri(folder, fileinfo)) for fileinfo in _folders]
		if not self.__folders: self.__aggregate()
		return False

	def __process(self, folder):
		self.__editor.response()
		self.__folders.append(folder)
		self.__manager.emit("get-fileinfos", folder)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __patch_cb(self, manager, folder):
		from gobject import idle_add
		idle_add(self.__process, folder)
		return False

	def __fileinfos_cb(self, manager, data):
		self.__get_files(data)
		return False
