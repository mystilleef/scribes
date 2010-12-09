from gio import Error, ERROR_NOT_FOUND

class GIOError(Error):

	def __init__(self):
		Error.__init__(self)
		self.code = ERROR_NOT_FOUND
		self.message = "TEST ERROR"

class Replacer(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("replace-file", self.__replace_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __error(self, data):
		self.__manager.emit("gio-error", data)
		return False

	def __test_error(self):
		raise Error, GIOError()

	def __replace(self, data):
		from gio import File, FILE_CREATE_NONE
		session_id, uri, encoding, text = data
		from glib import PRIORITY_DEFAULT
		File(uri).replace_async(self.__replace_async_cb,
			etag=None, make_backup=False, flags=FILE_CREATE_NONE,
			io_priority=PRIORITY_DEFAULT, cancellable=None, user_data=data)
		return False

	def __replace_async_cb(self, gfile, result, data):
		try:
			text = data[-1]
			if not text: raise AssertionError
			output_streamer = gfile.replace_finish(result)
			from glib import PRIORITY_DEFAULT
			output_streamer.write_async(text, self.__write_async_cb,
				io_priority=PRIORITY_DEFAULT, cancellable=None, user_data=data)
		except AssertionError:
			self.__manager.emit("finished", data)
		except Error, e:
			from gobject import idle_add
			idle_add(self.__error, (data, e))
		return False

	def __write_async_cb(self, output_streamer, result, data):
		try:
		#	raise self.__test_error()
			output_streamer.write_finish(result)
			from glib import PRIORITY_DEFAULT
			output_streamer.close_async(self.__close_async_cb, io_priority=PRIORITY_DEFAULT,
			cancellable=None, user_data=data)
		except Error, e:
			from gobject import idle_add
			idle_add(self.__error, (data, e))
		return False

	def __close_async_cb(self, output_streamer, result, data):
		try:
			output_streamer.close_finish(result)
			self.__manager.emit("finished", data)
		except Error, e:
			from gobject import idle_add
			idle_add(self.__error, (data, e))
		return False

	def __replace_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__replace, data)
		return False
