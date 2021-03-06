class Filterer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("formatted-files", self.__files_cb)
		self.__sigid3 = manager.connect("pattern", self.__pattern_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__files = []
		self.__pattern = ""
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		return False

	def __is_a_match(self, pattern, _file):
		self.__editor.refresh(False)
		if self.__pattern != pattern: raise AssertionError
		return pattern.lower() in _file.lower()

	def __filter(self, pattern):
		try:
			self.__editor.refresh(False)
			if not pattern: raise ValueError
			filtered_files = [(_file, uri) for _file, uri in self.__files if self.__is_a_match(pattern, _file)]
			self.__manager.emit("filtered-files", filtered_files)
		except ValueError:
			self.__manager.emit("filtered-files", [])
		except AssertionError:
			return False
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __files_cb(self, manager, files):
		self.__files = files
		return False

	def __pattern_cb(self, manager, pattern):
		self.__pattern = pattern
		self.__remove_timer()
		from gobject import idle_add
		self.__timer = idle_add(self.__filter, pattern)
		return False
