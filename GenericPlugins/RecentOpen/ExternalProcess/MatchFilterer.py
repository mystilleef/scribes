from SCRIBES.SignalConnectionManager import SignalManager

class Filterer(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "recent-infos-data", self.__data_cb)
		self.connect(manager, "search-pattern", self.__pattern_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__pattern = ""
		self.__data = None
		self.__first_time = True
		return

	def __match_in(self, file_path, pattern):
		self.__manager.response()
		if self.__pattern != pattern: raise StandardError
		return pattern.lower() in file_path.lower()

	def __filter(self, pattern):
		try:
			self.__manager.response()
			if self.__data is None: return False
			if not pattern: raise ValueError
			filtered_data = [data for data in self.__data if self.__match_in(data[0], pattern)]
			self.__manager.emit("filtered-data", filtered_data)
		except ValueError:
			self.__manager.emit("filtered-data", self.__data)
		except StandardError:
			pass
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __data_cb(self, manager, data):
		self.__data = data
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer1 = idle_add(self.__filter, self.__pattern)
		return False

	def __pattern_cb(self, manager, pattern):
		self.__pattern = pattern
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer2 = idle_add(self.__filter, pattern)
		return False
