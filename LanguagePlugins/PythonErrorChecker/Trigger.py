from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)

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
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		return

	def __activate_cb(self, *args):
		self.__manager.activate()
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return
