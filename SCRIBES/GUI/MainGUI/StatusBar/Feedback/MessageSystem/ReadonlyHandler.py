from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

ENABLE_READONLY_MESSAGE = _("Enabled readonly mode")
READONLY_MESSAGE = _("File is in readonly mode")

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "readonly", self.__readonly_cb)
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

	def __set(self):
		self.__editor.update_message(ENABLE_READONLY_MESSAGE, "yes", 7)
		self.__editor.set_message(READONLY_MESSAGE)
		return False

	def __unset(self):
		self.__editor.unset_message(READONLY_MESSAGE)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __readonly_cb(self, editor, readonly):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__set if readonly else self.__unset, priority=PRIORITY_LOW)
		return False
