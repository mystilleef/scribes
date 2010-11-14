from SCRIBES.SignalConnectionManager import SignalManager

class Searcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "regex-object", self.__regex_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __find_matches(self, regex_object):
		iterator = regex_object.finditer(self.__editor.text.decode("utf-8"))
		matches = [match.span() for match in iterator]
		self.__manager.emit("found-matches", matches)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __regex_cb(self, manager, regex_object):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__find_matches, regex_object, priority=PRIORITY_LOW)
		return False
