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
		self.connect(self.__trigger3, "activate", self.__activate_cb)
		self.connect(editor.textview, "populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"line-endings-to-unix", 
			"<alt>1", 
			_("Convert to unix line endings"), 
			_("Line Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"line-endings-to-mac", 
			"<alt>2", 
			_("Convert to mac line endings"), 
			_("Line Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"line-endings-to-windows", 
			"<alt>3", 
			_("Convert to windows line endings"), 
			_("Line Operations")
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

	def __create_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __activate_cb(self, trigger):
		if self.__manager is None: self.__manager = self.__create_manager()
		dictionary = {
			"line-endings-to-unix": self.__manager.to_unix,
			"line-endings-to-windows": self.__manager.to_windows,
			"line-endings-to-mac": self.__manager.to_mac,
		}
		dictionary[trigger.name]()
		return False

	def __popup_cb(self, textview, menu):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False
