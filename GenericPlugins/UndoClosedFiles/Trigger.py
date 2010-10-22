from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)
		self.connect(self.__trigger1, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		name, shortcut, description, category = (
			"reopen-closed-file", 
			"<ctrl><shift>w", 
			_("Reopen last closed file"), 
			_("File Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		self.__trigger.command = "open-last-file"
		name, shortcut, description, category = (
			"reopen-closed-files", 
			"<ctrl><shift>q", 
			_("Reopen last closed file"), 
			_("File Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		self.__trigger1.command = "open-last-files"
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __activate(self, trigger):
		self.__manager.activate(trigger.command)
		return False

	def __activate_cb(self, trigger):
		from gobject import idle_add
		idle_add(self.__activate, trigger)
		return False
