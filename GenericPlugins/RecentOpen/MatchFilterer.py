from SCRIBES.SignalConnectionManager import SignalManager

class Filterer(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "recent-infos-data", self.__data_cb)
		self.connect(manager, "search-pattern", self.__pattern_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__pattern = ""
		self.__data = None
		self.__first_time = True
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __match_in(self, file_path, pattern):
		self.__editor.refresh()
		if self.__pattern != pattern: raise StandardError
		return pattern.lower() in file_path.lower()

	def __filter(self, pattern):
		try:
			self.__editor.refresh()
			if self.__data is None: return False
			if not pattern: raise ValueError
			filtered_data =[data for data in self.__data if self.__match_in(data[0], pattern)]
			self.__manager.emit("filtered-data", filtered_data)
		except ValueError:
			self.__manager.emit("filtered-data", self.__data)
		except StandardError:
			pass
		return False

	def __filter_timeout(self, pattern):
		from gobject import idle_add
		self.__timer = idle_add(self.__filter, pattern)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __data_cb(self, manager, data):
		self.__data = data
		if self.__first_time: self.__filter("")
		self.__first_time = False
		return False

	def __pattern_cb(self, manager, pattern):
		try:
			self.__editor.refresh(False)
			self.__pattern = pattern
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__filter, pattern, priority=9999)
		return False
