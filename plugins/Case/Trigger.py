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
		self.__manager = None
		name, shortcut, description, category = (
			"togglecase", 
			"<alt>u", 
			_("Convert the case of text"), 
			_("Text Manipulation")
		)		
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"titlecase", 
			"<alt><shift>u", 
			_("Convert text to title case"), 
			_("Text Manipulation")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"swapcase", 
			"<alt><shift>l", 
			_("Swap the case of text"), 
			_("Text Manipulation")
		)
		self.__trigger3 = self.create_trigger(name, shortcut, description, category)
		return

	def __destroy(self):
		self.disconnect()
		self.remove_triggers()
		del self
		return False

	def __create_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __activate_cb(self, trigger):
		if self.__manager is None: self.__manager = self.__create_manager()
		triggers = {"togglecase": self.__manager.toggle,
					"titlecase": self.__manager.title,
					"swapcase": self.__manager.swap}
		triggers[trigger.name]()
		return False

	def __popup_cb(self, *args):
		from PopupMenuItem import PopupMenuItem
		self.__editor.add_to_popup(PopupMenuItem(self.__editor))
		return False

	def destroy(self):
		self.__destroy()
		return
