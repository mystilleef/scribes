from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "readonly-error", self.__error_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __error(self):
		from gettext import gettext as _
		message = _("ERROR: Failed to perform operation in readonly mode")
		self.__editor.update_message(message, "fail")
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __error_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__error, priority=PRIORITY_LOW)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
