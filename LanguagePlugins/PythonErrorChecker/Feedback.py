from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "error-data", self.__message_cb)
		self.connect(manager, "remote-file-message", self.__error_cb)
		self.connect(manager, "check-message", self.__check_cb)

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

	def __message_cb(self, manager, data):
		if data[0]:
			message = "Error: %s on line %s" % (data[1], data[0])
			self.__editor.update_message(message, "error", 10)
		else:
			message = _("No errors found")
			self.__editor.update_message(message, "yes")
		return False

	def __error_cb(self, *args):
		message = _("No error checking on remote file")
		self.__editor.update_message(message, "no", 3)
		return False

	def __check_cb(self, *args):
		message = _("checking for errors please wait...")
		self.__editor.update_message(message, "run", 60)
		return False
