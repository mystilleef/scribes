class Spooler(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("new-job", self.__new_job_cb)
		manager.connect_after("finished", self.__finished_cb)
		manager.connect("ignored", self.__ignored_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		from collections import deque
		self.__jobs = deque()
		self.__busy = False
		return

	def __check(self):
		if self.__busy or not self.__jobs: return False
		self.__send(self.__jobs.pop())
		return False

	def __send(self, data):
		self.__busy = True
		self.__manager.emit("syntax-check", data)
		return False

	def __new_job_cb(self, manager, data):
		self.__jobs.appendleft(data)
		self.__check()
		return False

	def __finished_cb(self, *args):
		self.__busy = False
		self.__check()
		return False

	def __ignored_cb(self, *args):
		print "File has changed stopping analysis!"
		self.__busy = False
		self.__check()
		return False
