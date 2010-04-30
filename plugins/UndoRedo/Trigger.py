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
		name, shortcut, description, category = (
			"undo", 
			"<ctrl>z", 
			_("Undo last action"), 
			_("Text Operations")
		)
		self.__trigger1 = self.create_trigger(name, shortcut, description, category)
		name, shortcut, description, category = (
			"redo", 
			"<ctrl><shift>z", 
			_("Redo last action"), 
			_("Text Operations")
		)
		self.__trigger2 = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __activate_cb(self, trigger):
		function = {
			self.__trigger1: self.__editor.undo,
			self.__trigger2: self.__editor.redo,
		}
		function[trigger]()
		return
