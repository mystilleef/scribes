class Aggregator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-path", self.__path_cb)
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
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __get_uri(self, folder, fileinfo):
		self.__editor.response()
		from gio import File 
		from os.path import join
		path = join(File(folder).get_path(), fileinfo.get_name())
		return File(path).get_uri()

	def __update_afiles(self, afiles, folder, fileinfos):
		self.__editor.response()
		uris = [self.__get_uri(folder, fileinfo) for fileinfo in fileinfos]
		[afiles.append(_file) for _file in uris]
		return False

	def __aggregate(self):
		afiles = []
		[self.__update_afiles(afiles, folder, fileinfos) for folder, fileinfos in self.__files]
		self.__manager.emit("files", afiles)
		return False

	def __update_folder_and_files(self, fileinfo, _folders, _files):
		self.__editor.response()
		_files.append(fileinfo) if fileinfo.get_file_type() == 1 else _folders.append(fileinfo)
		return False

	def __update_files(self, data):
		self.__editor.response()
		folder, fileinfos = data
		_folders = []
		_files = []
		[self.__update_folder_and_files(fileinfo, _folders, _files) for fileinfo in fileinfos]
		self.__files.append((folder, _files))
		[self.__send_to_fileinfo_processor(self.__get_uri(folder, fileinfo)) for fileinfo in _folders]
		if folder in self.__folders: self.__folders.remove(folder)
		if not self.__folders: self.__aggregate()
		return False

	def __emit_children_documents(self, folder):
		self.__folders.clear()
		self.__files = []
		self.__send_to_fileinfo_processor(folder)
		return False

	def __send_to_fileinfo_processor(self, folder):
		self.__editor.response()
		self.__folders.append(folder)
		self.__manager.emit("get-fileinfos", folder)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __path_cb(self, manager, folder):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__emit_children_documents, folder)
		return False

	def __fileinfos_cb(self, manager, data):
		from gobject import idle_add
		self.__timer = idle_add(self.__update_files, data, priority=9999)
		return False
