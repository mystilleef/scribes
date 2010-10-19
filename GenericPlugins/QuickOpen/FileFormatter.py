class Formatter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-path", self.__path_cb)
		self.__sigid3 = manager.connect("files", self.__files_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__path = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __replace(self, _file):
		from gio import File
		_file = File(_file).get_parse_name()
		return _file.replace(self.__path, "").lstrip("/")

	def __format(self, files):
		paths = [self.__replace(_file) for _file in files]
		self.__manager.emit("formatted-files", paths)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __files_cb(self, manager, files):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__format, files)
		return False

	def __path_cb(self, manager, path):
		from gio import File
		self.__path = File(path).get_parse_name()
		return False
