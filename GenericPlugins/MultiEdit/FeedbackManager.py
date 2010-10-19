from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

DEFAULT_MESSAGE = _("Multi Editing Mode")

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "deactivate", self.__deactivate_cb)
		self.connect(manager, "add-edit-point", self.__add_cb)
		self.connect(manager, "remove-edit-point", self.__remove_cb)
		self.connect(manager, "no-edit-point-error", self.__error_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		self.__editor.set_message(DEFAULT_MESSAGE)
		return False

	def __deactivate_cb(self, *args):
		message = _("Disabled multi editing mode")
		self.__editor.update_message(message, "yes")
		self.__editor.unset_message(DEFAULT_MESSAGE)
		return False

	def __add_cb(self, *args):
		message = _("New edit point")
		self.__editor.update_message(message, "yes")
		return False

	def __remove_cb(self, *args):
		message = _("Removed edit point")
		self.__editor.update_message(message, "cut")
		return False

	def __error_cb(self, *args):
		message = _("ERROR: No edit points found")
		self.__editor.update_message(message, "no")
		return False
