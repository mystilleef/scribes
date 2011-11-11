class Manager(object):

	def __init__(self):
		from collections import deque
		self.__timers = deque()

	def add(self, *args):
		[self.__timers.append(timer) for timer in args if timer not in self.__timers]
		return False

	def delete(self, *args):
		return self.remove(*args)

	def remove(self, *args):
		[self.__remove(timer) for timer in args if timer in self.__timers]
		return False

	def remove_all(self):
		from copy import copy
		[self.remove(timer) for timer in copy(self.__timers)]
		return False

	def destroy(self):
		self.remove_all()
		self.__timers.clear()
		del self.__timers
		del self
		return False

	def __remove(self, timer):
		self.__timers.remove(timer)
		from gobject import source_remove
		source_remove(timer)
		return
