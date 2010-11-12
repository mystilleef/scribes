from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
#		self.connect(self.__trigger1, "activate", self.__activate_cb)
#		self.connect(self.__trigger2, "activate", self.__activate_cb)
		self.connect(self.__trigger3, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
#		name, shortcut, description, category = (
#			"scroll-up", 
#			"<ctrl>Up", 
#			_("Scroll editing area up"), 
#			_("Navigation Operations")
#		)
#		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
#		name, shortcut, description, category = (
#			"scroll-down", 
#			"<ctrl>Down", 
#			_("Scroll editing area down"), 
#			_("Navigation Operations")
#		)
#		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"center", 
			"<alt>m", 
			_("Move cursor line to center"), 
			_("Navigation Operations")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __get_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __activate_cb(self, trigger):
		if not self.__manager: self.__manager = self.__get_manager()
		function = {
#			self.__trigger1: self.__manager.scroll_up,
#			self.__trigger2: self.__manager.scroll_down,
			self.__trigger3: self.__manager.center,
		}
		function[trigger]()
		return
