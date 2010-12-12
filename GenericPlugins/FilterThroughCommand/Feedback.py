from gettext import gettext as _

from SCRIBES.SignalConnectionManager import SignalManager

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "execute", self.__execute_cb)
		self.connect(manager, "hide", self.__hide_cb)
		self.connect(manager, "win", self.__win_cb, True)
		self.connect(manager, "fail", self.__fail_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __fail_cb(self, *args):
		message = _("ERROR: command failed to execute")
		self.__editor.update_message(message, "no", 10)
		return False

	def __win_cb(self, *args):
		message = _("command executed successfully")
		self.__editor.update_message(message, "yes", 5)
		return False

	def __execute_cb(self, *args):
#		message = _("please wait...")
#		self.__editor.update_message(message, "run", 600)
		return False

	def __hide_cb(self, *args):
		self.__editor.hide_message()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
