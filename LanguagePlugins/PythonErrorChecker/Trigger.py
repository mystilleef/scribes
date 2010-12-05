from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger1, "activate", self.__activate_cb)
		self.connect(self.__trigger2, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		name, shortcut, description, category = (
			"move-cursor-to-errors",
			"F2",
			_("Move cursor to errors in python code"),
			_("Python"),
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		self.__trigger1.command = "activate"
		name, shortcut, description, category = (
			"toggle-error-checking",
			"<shift>F2",
			_("Move cursor to errors in python code"),
			_("Python"),
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__trigger2.command = "toggle-error-check"
		return

	def __activate_cb(self, trigger):
		self.__manager.activate(trigger.command)
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return
