class Checker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("check-file-type", self.__check_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		return False

	def __error(self, data):
		self.__manager.emit("gio-error", data)
		return False

	def __raise_error(self):
		from gio import Error, ERROR_NOT_REGULAR_FILE
		message = "ERROR: Not a regular file."
		from GIOError import GError
		raise Error, (GError(ERROR_NOT_REGULAR_FILE, message))

	def __check(self, uri):
		from gio import File
		File(uri).query_info_async(self.__async_result_cb, "standard::type")
		return False

	def __async_result_cb(self, gfile, result):
		from gio import FILE_TYPE_REGULAR, Error
		try:
			from gobject import idle_add
			fileinfo = gfile.query_info_finish(result)
			if fileinfo.get_file_type() != FILE_TYPE_REGULAR: self.__raise_error()
			idle_add(self.__manager.emit, "read-uri", gfile.get_uri())
		except Error, e:
			idle_add(self.__error, (gfile, e))
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __check_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__check, uri)
		return False
