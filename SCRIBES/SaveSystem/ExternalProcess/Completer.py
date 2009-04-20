class Completer(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("finished", self.__finished_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __emit(self, data):
		# data = (session_id, uri, encoding)
		data = data[0], data[1], data[2]
		self.__manager.emit("saved-data", data)
		return False

	def __finished_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__emit, data)
		return False
