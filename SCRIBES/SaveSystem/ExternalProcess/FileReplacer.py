class Replacer(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("replace-file", self.__replace_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __replace(self, data):
		session_id, uri, encoding, text = data
		from gio import File, FILE_CREATE_NONE
		File(uri).replace_contents_async(text, self.__ready_cb,
			etag=None, make_backup=False, flags=FILE_CREATE_NONE,
			cancellable=None, user_data=data)
#		File(uri).replace_contents(text, etag=None, make_backup=False,
#			flags=FILE_CREATE_NONE, cancellable=None)
#		self.__manager.emit("finished", data)
		return False

	def __emit(self, result, data):
		print "one"
		success = result.get_source_object().replace_contents_finish(result)
		print "two"
		self.__manager.emit("finished", data)
		return False

	def __cancel(self, *args):
		return False

	def __ready_cb(self, gfile, result, data):
		print gfile
		from gobject import idle_add
		idle_add(self.__emit, result, data)
		return False

	def __replace_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__replace, data)
		return False
