from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

FEEDBACK_MESSAGE = _("Open recent files")

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		editor.refresh()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__row_cb)
		self.connect(manager, "search-pattern", self.__search_cb)
		self.connect(manager, "filtered-data", self.__data_cb)
		self.connect(manager, "selected-row", self.__row_cb)
		editor.refresh()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__pattern = ""
		self.__matches = 0
		return

	def __update_message(self, data, time):
		self.__manager.emit("message", data)
		self.__hide_after(time)
		return False

	def __hide(self):
		self.__manager.emit("hide-message")
		return False

	def __hide_after(self, time):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(time*1000, self.__hide)
		return False

	def __set_message(self):
		if not self.__pattern:
			message = _("%s files") if self.__matches else _("No files")
			if self.__matches == 1: message = _("%s file")
		else:
			message = _("%s matches found") if self.__matches else _("No match found")
			if self.__matches ==1: message = _("%s match found")
		time = 10
		message_type = "INFO" if self.__matches else "ERROR"
		message = message % str(self.__matches) if self.__matches else message
		data = (message_type, message)
		self.__update_message(data, time)
		return False

	def __search_message(self):
		data = ("PROGRESS", _("Searching please wait..."))
		self.__update_message(data, 21)
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __search_cb(self, manager, pattern):
		try:
			self.__pattern = pattern
			from gobject import timeout_add, source_remove
			source_remove(self.__timer2)
		except AttributeError:
			pass
		finally:
			self.__timer2 = timeout_add(250, self.__search_message, priority=9999)
		return False

	def __data_cb(self, manager, data):
		self.__matches = len(data)
		return False

	def __row_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer2)
		except AttributeError:
			pass
		finally:
			idle_add(self.__set_message, priority=9999)
		return False
