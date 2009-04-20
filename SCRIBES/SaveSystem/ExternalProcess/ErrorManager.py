class Manager(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("oops", self.__error_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __error(self, data):
		print data[-1]
		return False

	def __error_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__error, data)
		return False
