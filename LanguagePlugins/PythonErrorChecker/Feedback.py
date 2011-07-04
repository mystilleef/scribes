from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "error-data", self.__message_cb, True)
		self.connect(manager, "remote-file-message", self.__error_cb)
		self.connect(manager, "check-message", self.__check_cb)
		self.connect(manager, "error-check-type", self.__type_cb, True)
		self.connect(manager, "toggle-error-check", self.__toggle_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		from collections import deque
		self.__messages = deque()
		self.__editor = editor
		self.__is_first_time = True
		return

	def __unset_last_message(self):
		if not self.__messages: return False
		message = self.__messages.pop()
		self.__editor.unset_message(message, "error")
		# self.__editor.hide_message()
		return False

	def __show_message(self, data):
		if data[0]:
			message = "Error: %s on line %s" % (data[1], data[0])
			if self.__messages and (self.__messages[-1] == message): return False
			self.__unset_last_message()
			self.__messages.append(message)
			self.__editor.update_message(message, "error", 3000)
			self.__editor.set_message(message, "error")
		else:
			self.__unset_last_message()
			message = _("No errors found")
			self.__editor.update_message(message, "yes")
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __message_cb(self, manager, data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__show_message, data, priority=PRIORITY_LOW)
		return False

	def __error_cb(self, *args):
		message = _("No error checking on remote file")
		self.__editor.update_message(message, "no", 3)
		return False

	def __check_cb(self, *args):
		message = _("checking for errors please wait...")
		self.__editor.update_message(message, "run", 10)
		return False

	def __type_cb(self, manager, more_error_checks):
		from Exceptions import FirstTimeError
		try:
			if self.__is_first_time: raise FirstTimeError
			message = _("Switched to Python error checking") if more_error_checks else _("Switched to syntax error checking")
			self.__editor.hide_message()
			self.__editor.update_message(message, "yes")
		except FirstTimeError:
			self.__is_first_time = False
		return False

	def __toggle_cb(self, *args):
		message = _("switching please wait...")
		self.__editor.update_message(message, "run", 20)
		return False
