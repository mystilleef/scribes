from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__show_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		name, shortcut, description, category = ("show-python-symbol-brower", "F5", _("Show classes, methods and functions"), _("Python"))
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		return

	def __show_cb(self, *args):
		try:
			self.__manager.show_browser()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.show_browser()
		return

	def destroy(self):
		if self.__manager: self.__manager.destroy()
		self.disconnect()
		self.remove_triggers()
		del self
		return

