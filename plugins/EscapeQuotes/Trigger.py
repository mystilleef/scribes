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
		from Manager import Manager
		self.__manager = Manager(editor)
		name, shortcut, description, category = (
			"escape-quotes",
			"<ctrl><shift>e",
			_("Escape quotes"),
			_("Text Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"unescape-quotes",
			"<ctrl><alt>e",
			_("Unescape quotes"),
			_("Text Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __activate_cb(self, trigger):
		function = {
			self.__trigger1: self.__manager.escape,
			self.__trigger2: self.__manager.unescape,
		}
		function[trigger]()
		return False
