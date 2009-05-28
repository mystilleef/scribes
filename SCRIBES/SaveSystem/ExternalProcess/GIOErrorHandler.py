class Handler(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("gio-error", self.__error_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __error(self, data):
		data, error = data
		data = data + (error.message,)
		self.__manager.emit("oops", data)
		return False

	def __error_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__error, data)
		return False
