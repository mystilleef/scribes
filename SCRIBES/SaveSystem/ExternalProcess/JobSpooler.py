class Spooler(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("save-data", self.__new_job_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __send(self, data):
		from gobject import idle_add
		idle_add(self.__manager.emit, "encode-text", data)
		return False

	def __new_job_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__send, data)
		return False
