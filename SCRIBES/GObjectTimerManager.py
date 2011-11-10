class Manager(object):

	def __init__(self):
		from collections import deque
		self.__timers = deque()
		print "Initialized GObject Timer Manager"

	def add(self, timer):
		if timer in self.__timers: return False
		self.__timers.append(timer)
		print "Added new GObject timer"
		return False

	def remove(self, timer):
		if timer not in self.__timers: return False
		self.__timers.remove(timer)
		from gobject import source_remove
		source_remove(timer)
		print "Removed Gobject timer ", timer
		return False

	def delete(self, timer):
		return self.remove(timer)

	def remove_all(self):
		from copy import copy
		[self.remove(timer) for timer in copy(self.__timers)]
		return False

	def destroy(self):
		self.remove_all()
		self.__timers.clear()
		del self.__timers
		del self
		print "Destroyed GObject Timer Manager"
		return False
