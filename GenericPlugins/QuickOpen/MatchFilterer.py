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
		self.__timer = 1
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		return False

	def __is_a_match(self, pattern, _file):
		self.__editor.refresh()
		if self.__pattern != pattern: raise StandardError
		if pattern.lower() in _file: return 2
		index = 0
		for character in pattern:
			index = _file.lower().find(character.lower(), index)
			if index == -1: return 0
		return 1

	def __is_a_match_re(self, pattern, _file):
		self.__editor.refresh()
		if self.__pattern != pattern: raise StandardError
		from fnmatch import translate
		pattern = r"%s" % translate(pattern).replace("\Z(?ms)", "")
		from re import search, U, I, error
		flags = U | I
		try:
			return search(pattern, _file, flags)
		except error:
			return False

	def __filter(self, pattern):
		try:
			self.__editor.refresh()
			if not pattern: raise ValueError
			matches = [_file for _file in self.__files if self.__is_a_match_re(pattern, _file)]
#			higher_matches = []
#			lower_matches = []
#			for _file in self.__files:
#				self.__editor.refresh()
#				rank = self.__is_a_match(pattern, _file)
#				if not rank: continue
#				higher_matches.append(_file) if rank == 2 else lower_matches.append(_file)
#			matches = higher_matches + lower_matches
			self.__manager.emit("filtered-files", matches)
		except ValueError:
			self.__manager.emit("filtered-files", [])
		except StandardError:
			return False
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __files_cb(self, manager, files):
		self.__files = files
		return False

	def __pattern_cb(self, manager, pattern):
		try:
			self.__pattern = pattern
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__filter, pattern)
		return False
