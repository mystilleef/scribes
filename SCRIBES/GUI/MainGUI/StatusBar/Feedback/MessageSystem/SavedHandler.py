from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "saved-file", self.__saved_cb)
		self.connect(editor, "save-error", self.__error_cb)
		self.connect(manager, "busy", self.__busy_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __saved_cb(self, *args):
		if self.__busy: return False
		self.__editor.update_message(_("Saved file"), "save", 3, "low")
		return False

	def __error_cb(self, *args):
		message = _("Failed to save file")
		self.__editor.update_message(message, "no", 10, "high")
		return False

	def __busy_cb(self, manager, busy):
		self.__busy = busy
		return False
