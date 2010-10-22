from glib import PRIORITY_LOW
from gobject import timeout_add, idle_add, source_remove
from SCRIBES.SignalConnectionManager import SignalManager

class Timer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(editor.textbuffer, "changed", self.__changed_cb, True)
		self.__check_timeout()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __check(self):
		self.__manager.emit("check")
		return False

	def __check_timeout(self):
		self.__timer = idle_add(self.__check, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		try:
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(5000, self.__check_timeout, priority=PRIORITY_LOW)
		return False

	def __activate_cb(self, *args):
		try:
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__check, priority=PRIORITY_LOW)
		return False
