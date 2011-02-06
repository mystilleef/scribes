class Spooler(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("new-job", self.__new_job_cb)
		manager.connect_after("finished", self.__finished_cb)
		manager.connect_after("no-change", self.__finished_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__busy = False
		self.__new_job = False
		return

	def __check(self):
		if self.__busy or self.__new_job is False: return False
		self.__new_job = False
		self.__busy = True
		self.__manager.emit("index-request")
		return False

	def __new_job_cb(self, manager, data):
		self.__new_job = True
		from gobject import idle_add
		idle_add(self.__check)
		return False

	def __finished_cb(self, *args):
		self.__busy = False
		from gobject import idle_add
		idle_add(self.__check)
		return False
