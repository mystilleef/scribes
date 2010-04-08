from gettext import gettext as _
from gtk import PRINT_STATUS_INITIAL, PRINT_STATUS_PREPARING
from gtk import PRINT_STATUS_GENERATING_DATA, PRINT_STATUS_SENDING_DATA
from gtk import PRINT_STATUS_FINISHED, PRINT_STATUS_FINISHED_ABORTED
from SCRIBES.SignalConnectionManager import SignalManager

CANCEL_MESSAGE = _("Cancelled print operation")
INITIAL_MESSAGE = _("Print file")

PRINTING = {
	PRINT_STATUS_INITIAL: ("set_func", (_("Initializing print operation"), "printer")),
	PRINT_STATUS_PREPARING: ("set_func", (_("Preparing data for printing"), "printer")),
	PRINT_STATUS_GENERATING_DATA: ("set_func", (_("Generating data for printing"), "printer")),
	PRINT_STATUS_SENDING_DATA: ("set_func", (_("Sending file to printing"), "printer")),
	PRINT_STATUS_FINISHED: ("update_func", (_("Finished printing file"), "yes", 10)),
	PRINT_STATUS_FINISHED_ABORTED: ("update_func", (_("Aborted print operation"), "no", 10)),
}

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "feedback", self.__feedback_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "cancel", self.__cancel_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__stack = deque()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, status):
		self.__editor.response()
		previous_status_message = self.__stack.pop()
		function, args = PRINTING[status]
		self.__stack.append(args[0])
		self.__editor.unset_message(previous_status_message, "printer")
		update = self.__editor.set_message if function == "set_func" else self.__editor.update_message
		update(*args)
		return False

	def __feedback_cb(self, manager, status):
		self.__update(status)
		return False

	def __cancel_cb(self, *args):
		self.__editor.update_message(CANCEL_MESSAGE, "no")
		self.__editor.unset_message(INITIAL_MESSAGE, "printer")
		self.__stack.pop()
		return False

	def __activate_cb(self, *args):
		self.__editor.set_message(INITIAL_MESSAGE, "printer")
		self.__stack.append(INITIAL_MESSAGE)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
