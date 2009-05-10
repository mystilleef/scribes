class Replacer(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("replace-file", self.__replace_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__data = ()
		return

	def __replace(self, data):
		self.__data = data
		session_id, uri, encoding, text = data
		from gio import File
		File(uri).replace_contents_async(text, self.__ready_cb)
		return False

	def __ready_cb(self, gfile, result):
		success = gfile.replace_contents_finish(result)
		if success: self.__manager.emit("finished", self.__data)
		self.__data = ()
		return False

	def __replace_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__replace, data)
		return False
