from glib import PRIORITY_LOW
from gobject import idle_add, source_remove
from SCRIBES.SignalConnectionManager import SignalManager
from PyFlakes import checker

class Checker(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "check-tree", self.__check_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __check(self, tree):
		messages = checker.Checker(tree, self.__editor.filename).messages
		messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
		if messages: self.__manager.emit("tree-error", messages[0])
		signal = "errors-found" if messages else "no-errors-found"
		self.__manager.emit(signal)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, manager, tree):
		try:
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__check, tree, priority=PRIORITY_LOW)
		return False
