from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

CUT_MESSAGE = _("Cut operation")
COPY_MESSAGE = _("Copy operation")
PASTE_MESSAGE = _("Paste operation")

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(self.__editor, "quit", self.__destroy_cb)
		self.connect(self.__view, "copy-clipboard", self.__update_cb, True, (COPY_MESSAGE, "copy"))
		self.connect(self.__view, "cut-clipboard", self.__update_cb, True, (CUT_MESSAGE, "cut"))
		self.connect(self.__view, "paste-clipboard", self.__update_cb, True, (PASTE_MESSAGE, "paste"))
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.view
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update_cb(self, textview, data):
		message, image = data
		self.__editor.update_message(message, image, 3)
		return False
