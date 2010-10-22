from glib import PRIORITY_LOW
from gobject import timeout_add, idle_add, source_remove
from SCRIBES.SignalConnectionManager import SignalManager

class Rechecker(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "errors-found", self.__found_cb)
		self.connect(manager, "no-errors-found", self.__no_found_cb)
		self.connect(manager, "activate", self.__activate_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__show_message = False
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

	def __found_cb(self, *args):
		try:
			self.__show_message = True
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(15000, self.__check_timeout, priority=PRIORITY_LOW)
		return False

	def __no_found_cb(self, *args):
		if self.__show_message: self.__manager.emit("no-error-message")
		self.__show_message = False
		return False

	def __activate_cb(self, *args):
		self.__show_message = True
		return False
