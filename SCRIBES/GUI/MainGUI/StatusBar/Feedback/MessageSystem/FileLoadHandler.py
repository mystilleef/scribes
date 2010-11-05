from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

BUSY_MESSAGE = _("Loading file please wait...")
SUCCESS_MESSAGE = _("Loaded file")
ERROR_MESSAGE = _("ERROR: Failed to load file")

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "checking-file", self.__checking_cb)
		self.connect(editor, "loaded-file", self.__loaded_cb)
		self.connect(editor, "load-error", self.__error_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, *args):
		self.__editor.update_message(BUSY_MESSAGE, "run", 1000)
		return False

	def __loaded_cb(self, *args):
		self.__editor.update_message(SUCCESS_MESSAGE, "open")
		return False

	def __error_cb(self, *args):
		self.__editor.update_message(ERROR_MESSAGE, "fail", 10)
		return False
