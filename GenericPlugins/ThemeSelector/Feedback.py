from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

FEEDBACK_MESSAGE = _("Manage themes")

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "schemes", self.__schemes_cb)
		self.connect(manager, "valid-scheme-files", self.__schemes_cb)
		self.connect(manager, "delete-row", self.__schemes_cb)
		self.connect(manager, "row-changed", self.__changed_cb)
		self.connect(manager, "theme-from-database", self.__database_cb)
		self.connect(manager, "delete-error", self.__error_cb)
		self.connect(manager, "new-scheme", self.__new_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "hide-window", self.__hide_cb)
		self.connect(manager, "invalid-scheme-files", self.__invalid_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__scheme = None
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

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __schemes_cb(self, *args):
		if not self.__scheme: return False
		data = ("PROGRESS", _("Updating themes please wait..."))
		self.__update_message(data, 7)
		return False

	def __changed_cb(self, *args):
		data = ("PROGRESS", _("Changing theme please wait..."))
		self.__update_message(data, 7)
		return False

	def __database_cb(self, manager, theme):
		if not self.__scheme: return False
		data = ("INFO", _("Theme is now set to '%s'") % self.__scheme.get_name())
		self.__update_message(data, 10)
		return False

	def __error_cb(self, *args):
		data = ("ERROR", _("Error: Cannot remove default themes"))
		self.__update_message(data, 10)
		return False

	def __invalid_cb(self, *args):
		data = ("ERROR", _("Error: No valid theme files found"))
		self.__update_message(data, 10)
		return False

	def __new_cb(self, manager, scheme):
		self.__scheme = scheme
		return False

	def __activate_cb(self, *args):
		self.__editor.set_message(FEEDBACK_MESSAGE)
		return False

	def __hide_cb(self, *args):
		self.__editor.unset_message(FEEDBACK_MESSAGE)
		return False
