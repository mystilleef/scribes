class Handler(object):

	def __init__(self, manager):
		self.__manager = manager
		from signal import signal, SIGHUP, SIGTERM, SIGABRT, SIGSEGV
		signal(SIGTERM, self.__quit_cb)
		signal(SIGHUP, self.__quit_cb)
		signal(SIGABRT, self.__quit_cb)
		signal(SIGSEGV, self.__quit_cb)

	def __quit_cb(self, signum, frame):
		self.__manager.close_all_windows()
		return
