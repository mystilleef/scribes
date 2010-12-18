from gettext import gettext as _

from SCRIBES.SignalConnectionManager import SignalManager

SPARKUP_MESSAGE = _("Sparkup mode")

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "inserted-template", self.__inserted_cb, True)
		self.connect(manager, "exit-sparkup-mode", self.__exit_cb, True)
		self.connect(manager, "next-placeholder", self.__next_cb, True)
		self.connect(manager, "previous-placeholder", self.__previous_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__nesting_level = 0
		return

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __inserted_cb(self, *args):
		if not self.__nesting_level: self.__editor.set_message(SPARKUP_MESSAGE)
		self.__nesting_level += 1
		return False

	def __exit_cb(self, *args):
		self.__nesting_level -= 1
		if self.__nesting_level < 0: self.__nesting_level = 0
		if self.__nesting_level: return False
		self.__editor.unset_message(SPARKUP_MESSAGE)
		self.__editor.update_message(_("leaving sparkup mode"), "yes")
		return False

	def __next_cb(self, *args):
		self.__editor.update_message(_("Next placeholder"), "yes")
		return False

	def __previous_cb(self, *args):
		self.__editor.update_message(_("Previous placeholder"), "yes")
		return False
